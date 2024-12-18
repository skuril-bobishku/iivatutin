package main

import (
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/skuril-bobishku/iivatutin/backend/internal/config"
	"github.com/skuril-bobishku/iivatutin/backend/internal/server"
	"log"
)

func main() {
	fiberCFG := fiber.Config{
		BodyLimit: 200 * 1024 * 1024,
	}

	app := fiber.New(fiberCFG)
	app.Use(cors.New())

	app.Use(cors.New())

	server.SetRoutes(app)

	if err := app.Listen(":" + config.SetServerPort()); err != nil {
		log.Fatalf("Ошибка: %v", err)
	}
}
