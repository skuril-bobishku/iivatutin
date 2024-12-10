package server

import "github.com/gofiber/fiber/v2"

func SetRoutes(app *fiber.App) {
	app.Post("/upload", uploadZIP)
	app.Get("/parse", parseImages)
	app.Get("/train", trainYOLO)
}
