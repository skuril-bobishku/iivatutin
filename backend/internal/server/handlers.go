package server

import (
	"github.com/gofiber/fiber/v2"
	"github.com/skuril-bobishku/iivatutin/backend/internal/config"
	"path/filepath"
)

func UploadZIP(c *fiber.Ctx) error {
	directory := config.GetServerDirectory()

	status := saveZIP(c, directory)
	code, json := status()
	filename, exists := json["path"].(string)
	if !exists {
		return c.Status(code).JSON(json)
	}

	status = unzip(c, directory, filename)
	code, json = status()
	return c.Status(code).JSON(json)
}

func ParseImages(c *fiber.Ctx) error {
	var url string
	var count, skip int
	images := &[]string{}

	status := checkQuery(c, &url, &count, &skip)
	code, json := status()
	if code != fiber.StatusContinue {
		return c.Status(code).JSON(json)
	}

	status = parseIMG(url, count, skip, images)
	code, json = status()
	if code != fiber.StatusAccepted {
		return c.Status(code).JSON(json)
	}

	dir := config.GetServerDirectory()
	dir = filepath.Join(dir, getUrlName(url, 2))

	status = downloadImages(dir, images)
	code, json = status()
	return c.Status(code).JSON(json)
}

func StartTrainYOLO(c *fiber.Ctx) error {
	files := []fiber.Map{
		{"id": 1, "name": "123"},
		{"id": 2, "name": "456"},
	}

	return c.JSON(files)
}
