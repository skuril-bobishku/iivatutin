package server

import "github.com/gofiber/fiber/v2"

func SendStatus(c *fiber.Ctx, typeErr func() (int, fiber.Map)) {
	statusCode, jsonMap := typeErr()
	c.Status(statusCode).JSON(jsonMap)
	c.Context().Done()
}

func CheckStatus(c *fiber.Ctx, err error, typeErr func() (int, fiber.Map)) {
	if err != nil {
		SendStatus(c, typeErr)
	}
}
