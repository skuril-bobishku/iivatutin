package server

import (
	"archive/zip"
	"github.com/gofiber/fiber/v2"
	"github.com/skuril-bobishku/iivatutin/backend/internal/config"
	"io"
	"os"
	"path/filepath"
	"strings"
)

func UploadZIP(c *fiber.Ctx) error {
	file, err := c.FormFile("file")
	CheckStatus(c, err, NotRequired)

	if filepath.Ext(file.Filename) != ".zip" {
		SendStatus(c, BadFileFormat)
	}

	dir := config.GetServerDirectory()

	_, err = os.Stat(dir)
	if os.IsNotExist(err) {
		err = os.Mkdir(dir, os.ModePerm)
		CheckStatus(c, err, NotCreatedDirectory)
	}

	uploadPath := dir + "/" + file.Filename
	err = c.SaveFile(file, uploadPath)
	CheckStatus(c, err, NotSavedFile)

	r, err := zip.OpenReader(uploadPath)
	CheckStatus(c, err, NotOpenZIP)
	defer r.Close()

	for _, f := range r.File {
		filePath := filepath.Join(dir, f.Name)

		relPath, err := filepath.Rel(filePath, dir)
		CheckStatus(c, err, NotRelativePath)

		if !filepath.IsAbs(relPath) && !strings.HasPrefix(relPath, "..") {
			SendStatus(c, NotSafePath)
		}

		if f.FileInfo().IsDir() {
			err = os.Mkdir(filePath, os.ModePerm)
			CheckStatus(c, err, NotCreatedDirectory)
			continue
		}

		err = os.MkdirAll(filepath.Dir(filePath), os.ModePerm)
		CheckStatus(c, err, NotCreatedDirectory)

		outFile, err := os.OpenFile(filePath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, f.Mode())
		CheckStatus(c, err, NotOpenFile)
		defer outFile.Close()

		rc, err := f.Open()
		CheckStatus(c, err, NotOpenFile)
		defer rc.Close()

		_, err = io.Copy(outFile, rc)
		CheckStatus(c, err, NotCopyFile)
	}

	return c.Status(fiber.StatusContinue).JSON(fiber.Map{
		"status":  "success",
		"message": "File uploaded successfully",
		"path":    uploadPath,
	})
}

func StartTrainYOLO(c *fiber.Ctx) error {
	files := []fiber.Map{
		{"id": 1, "name": "123"},
		{"id": 2, "name": "456"},
	}

	return c.JSON(files)
}
