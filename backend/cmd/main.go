package main

import (
	"github.com/gofiber/fiber/v2"
	"github.com/skuril-bobishku/iivatutin/backend/internal/config"
	"github.com/skuril-bobishku/iivatutin/backend/internal/server"
	"log"
)

func main() {
	fiberCFG := fiber.Config{
		BodyLimit: 200 * 1024 * 1024,
	}

	app := fiber.New(fiberCFG)

	server.SetRoutes(app)

	if err := app.Listen(":" + config.SetServerPort()); err != nil {
		log.Fatalf("Ошибка: %v", err)
	}
}
