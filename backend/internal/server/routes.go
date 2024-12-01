package server

import "github.com/gofiber/fiber/v2"

func SetRoutes(app *fiber.App) {
	app.Post("/upload", UploadZIP)
	app.Get("/train", StartTrainYOLO)
}
