package status_ctx

import "github.com/gofiber/fiber/v2"

func NotRequiredUrl() (int, fiber.Map) {
	return fiber.StatusBadRequest,
		fiber.Map{"error": "Not 'url' in query"}
}

func NotRequiredCount() (int, fiber.Map) {
	return fiber.StatusBadRequest,
		fiber.Map{"error": "Not 'count' in query"}
}

func BadParsing() (int, fiber.Map) {
	return fiber.StatusInternalServerError,
		fiber.Map{"error": "Failed to parsing page"}
}

func NotNumericCount() (int, fiber.Map) {
	return fiber.StatusInternalServerError,
		fiber.Map{"error": "Not a number in 'count'"}
}
