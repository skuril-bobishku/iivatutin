package status_ctx

import "github.com/gofiber/fiber/v2"

func NotRequired() (int, fiber.Map) {
	return fiber.StatusBadRequest,
		fiber.Map{"error": "Not required file"}
}

func BadFileFormat() (int, fiber.Map) {
	return fiber.StatusUnsupportedMediaType,
		fiber.Map{"error": "Not .zip file format"}
}

func NotCreatedDirectory() (int, fiber.Map) {
	return fiber.StatusInternalServerError,
		fiber.Map{"error": "Failed to create directory"}
}

func NotSavedFile() (int, fiber.Map) {
	return fiber.StatusInternalServerError,
		fiber.Map{"error": "Failed to save file"}
}

func FileSaved(path string) (int, fiber.Map) {
	return fiber.StatusContinue,
		fiber.Map{
			"message": "File was saved successfully",
			"path":    path,
		}
}

func NotOpenZIP() (int, fiber.Map) {
	return fiber.StatusInternalServerError,
		fiber.Map{"error": "Failed to open zip file"}
}

func NotRelativePath() (int, fiber.Map) {
	return fiber.StatusInternalServerError,
		fiber.Map{"error": "Failed to get relative path"}
}

func NotSafePath() (int, fiber.Map) {
	return fiber.StatusBadRequest,
		fiber.Map{"error": "Not safe path"}
}

func NotOpenFile() (int, fiber.Map) {
	return fiber.StatusInternalServerError,
		fiber.Map{"error": "Failed to open file"}
}

func NotCreateFile() (int, fiber.Map) {
	return fiber.StatusInternalServerError,
		fiber.Map{"error": "Failed to create file"}
}

func NotCopyFile() (int, fiber.Map) {
	return fiber.StatusInternalServerError,
		fiber.Map{"error": "Failed to copy file"}
}

func NotModifyFile() (int, fiber.Map) {
	return fiber.StatusInternalServerError,
		fiber.Map{"error": "Failed to modify file"}
}

func FileUnzip(path string) (int, fiber.Map) {
	return fiber.StatusCreated,
		fiber.Map{
			"message": "File was unzip successfully",
			"path":    path,
		}
}
