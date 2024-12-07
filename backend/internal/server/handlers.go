package server

import (
	"github.com/gofiber/fiber/v2"
	"github.com/skuril-bobishku/iivatutin/backend/internal/config"
)

func UploadZIP(c *fiber.Ctx) error {
	directory := config.GetServerDirectory()

	status := SaveZIP(c, directory)
	code, json := status()
	filename, exists := json["path"].(string)
	if !exists {
		return c.Status(code).JSON(json)
	}

	status = Unzip(c, directory, filename)
	code, json = status()
	return c.Status(code).JSON(json)
}

func ParseImages(c *fiber.Ctx) error {
	//dir := config.GetServerDirectory()

	CheckQuery(c)

	/*images, err := parseIMG(url, count)
	if err != nil {
		log.SendStatus(c, log.BadParsing)
	}*/

	return c.JSON(fiber.Map{
		/*"url":    url,
		"images": images,*/
	})
}

func StartTrainYOLO(c *fiber.Ctx) error {
	files := []fiber.Map{
		{"id": 1, "name": "123"},
		{"id": 2, "name": "456"},
	}

	return c.JSON(files)
}
