package server

import (
	"github.com/gofiber/fiber/v2"
	"github.com/playwright-community/playwright-go"
	"github.com/skuril-bobishku/iivatutin/backend/internal/config"
	stc "github.com/skuril-bobishku/iivatutin/backend/internal/server/status_ctx"
	"github.com/valyala/fasthttp"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
	"time"
)

func checkQuery(c *fiber.Ctx, url *string, count *int, skip *int) func() (int, fiber.Map) {
	maxCount := config.GetMaxImagesCount()

	*url = c.Query("url", "")
	if *url == "" {
		return stc.NotRequiredUrl
	}

	*count = c.QueryInt("count", maxCount)
	if *count == maxCount {
		return stc.NotRequiredCount
	}

	*skip = c.QueryInt("skip", 0)
	if *count > maxCount {
		*count = maxCount
	}

	return func() (int, fiber.Map) {
		return stc.RequireCorrectly(*url, strconv.Itoa(*count))
	}
}

func parseIMG(url string, count int, skip int, images *[]string) func() (int, fiber.Map) {
	pw, err := playwright.Run()
	if err != nil {
		return stc.NotRunningParser
	}
	defer pw.Stop()

	browser, err := pw.Chromium.Launch()
	if err != nil {
		return stc.NotLaunchChromium
	}
	defer browser.Close()

	page, err := browser.NewPage()
	if err != nil {
		return stc.NotOpenPage
	}

	_, err = page.Goto(url)
	if err != nil {
		return stc.NotOpenPage
	}

	_, err = page.WaitForSelector("div.photos div.TaxonPhoto.undefined div.CoverImage")
	if err != nil {
		return stc.NotWaitSelector
	}

	for i := 0; i < (skip+count)/25+1; i++ {
		_, err := page.Evaluate(`window.scrollTo(0, document.body.scrollHeight)`)
		if err != nil {
			return stc.NotEvaluatePage
		}
		time.Sleep(2 * time.Second)
	}

	elements, err := page.QuerySelectorAll("div.photos div.TaxonPhoto.undefined div.CoverImage")
	if err != nil {
		return stc.NotQuerySelector
	}

	re := regexp.MustCompile(`background-image:\s*url\(["']?(.*?)["']?\)`)
	for e, element := range elements {
		if e < skip {
			continue
		}

		if len(*images) >= count {
			break
		}

		style, err := element.GetAttribute("style")
		if err != nil || style == "" {
			continue
		}

		matches := re.FindStringSubmatch(style)
		if len(matches) > 1 {
			*images = append(*images, matches[1])
		}
	}

	return func() (int, fiber.Map) {
		return stc.ParsingCorrectly(*images)
	}
}

func getUrlName(url string, pos int) string {
	parts := strings.Split(url, "/")
	if len(parts) < 5 {
		return time.Now().Format("2006-01-02_15-04-05")
	}

	return parts[len(parts)-pos]
}

func downloadImages(dir string, images *[]string) func() (int, fiber.Map) {
	for _, img := range *images {
		client := &fasthttp.Client{}
		status, resp, err := client.Get(nil, img)
		if status != fiber.StatusOK && err != nil {
			return stc.BadUrlRequired
		}

		fileName := "img_" + getUrlName(img, 2) + filepath.Ext(img)
		filePath := filepath.Join(dir, fileName)
		err = os.MkdirAll(filepath.Dir(filePath), os.ModePerm)
		if err != nil {
			return stc.NotCreatedDirectory
		}

		outFile, err := os.Create(filePath)
		if err != nil {
			return stc.NotCreateFile
		}
		defer outFile.Close()

		_, err = outFile.Write(resp)
		if err != nil {
			return stc.NotCopyFile
		}
	}

	return func() (int, fiber.Map) {
		return stc.ImagesSaved(dir)
	}
}
