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

func NotNumericCount() (int, fiber.Map) {
	return fiber.StatusInternalServerError,
		fiber.Map{"error": "Not a number in 'count'"}
}

func RequireCorrectly(args ...string) (int, fiber.Map) {
	return fiber.StatusContinue,
		fiber.Map{
			"message": "File was saved successfully",
			"url":     args[0],
			"count":   args[1],
		}
}

func NotRunningParser() (int, fiber.Map) {
	return fiber.StatusInternalServerError,
		fiber.Map{"error": "Failed to run parser"}
}

func NotLaunchChromium() (int, fiber.Map) {
	return fiber.StatusInternalServerError,
		fiber.Map{"error": "Failed to launch chromium"}
}

func NotOpenPage() (int, fiber.Map) {
	return fiber.StatusInternalServerError,
		fiber.Map{"error": "Failed to open page"}
}

func NotWaitSelector() (int, fiber.Map) {
	return fiber.StatusInternalServerError,
		fiber.Map{"error": "Failed to wait for selector"}
}

func NotEvaluatePage() (int, fiber.Map) {
	return fiber.StatusInternalServerError,
		fiber.Map{"error": "Failed to scrolling page"}
}

func NotQuerySelector() (int, fiber.Map) {
	return fiber.StatusInternalServerError,
		fiber.Map{"error": "Failed to query selector all"}
}

func BadParsing() (int, fiber.Map) {
	return fiber.StatusInternalServerError,
		fiber.Map{"error": "Failed to parsing page"}
}

func ParsingCorrectly(images []string) (int, fiber.Map) {
	return fiber.StatusAccepted,
		fiber.Map{
			"message": "Images was parsed successfully",
			"images":  images,
		}
}

func BadUrlRequired() (int, fiber.Map) {
	return fiber.StatusConflict,
		fiber.Map{"error": "Failed require url"}
}

func ImagesSaved(path string) (int, fiber.Map) {
	return fiber.StatusOK,
		fiber.Map{
			"message": "Images was saved successfully",
			"path":    path,
		}
}
