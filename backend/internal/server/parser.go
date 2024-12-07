package server

import (
	"fmt"
	"github.com/gocolly/colly"
	"github.com/gofiber/fiber/v2"
)

func CheckQuery(c *fiber.Ctx) {
	//maxCount := config.GetMaxImagesCount()

	url := c.Query("url", "")
	fmt.Print(url)
	if url == "" {
		//stc.SendStatus(c, stc.NotRequiredUrl)
	}

	/*count := c.QueryInt("count", maxCount)
	if count == maxCount {
		log.SendStatus(c, log.NotRequiredCount)
	}

	cnt, err := strconv.Atoi(count)
	if err != nil {
		log.SendStatus(c, log.NotNumericCount)
	}

	if count > maxCount {
		count = maxCount
	}*/
}

func extractURL(style string) string {
	if len(style) > 5 && style[:4] == "url(" && style[len(style)-1] == ')' {
		return style[5 : len(style)-2]
	}
	return ""
}

func parseIMG(url string, maxImages int) ([]string, error) {
	var images []string

	collector := colly.NewCollector()
	collector.OnHTML("div[background-image]", func(e *colly.HTMLElement) {
		if len(images) >= maxImages {
			return
		}

		style := e.Attr("background-image")
		url := extractURL(style)
		if url != "" {
			images = append(images, url)
		}
	})

	collector.OnError(func(r *colly.Response, err error) {
		//log.Printf("Ошибка запроса к %s: %v", r.Request.URL, err)
	})

	err := collector.Visit(url)
	if err != nil {
		return nil, err
	}

	return images, nil
}
