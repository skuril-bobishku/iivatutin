package server

import (
	"archive/zip"
	"github.com/gofiber/fiber/v2"
	"github.com/skuril-bobishku/iivatutin/backend/internal/server/log"
	"io"
	"os"
	"path/filepath"
	"strings"
)

func SaveZIP(c *fiber.Ctx, directory string) string {
	file, err := c.FormFile("file")
	log.CheckStatus(c, err, log.NotRequired)

	if filepath.Ext(file.Filename) != ".zip" {
		log.SendStatus(c, log.BadFileFormat)
	}

	_, err = os.Stat(directory)
	if os.IsNotExist(err) {
		err = os.Mkdir(directory, os.ModePerm)
		log.CheckStatus(c, err, log.NotCreatedDirectory)
	}

	err = c.SaveFile(file, directory+file.Filename)
	log.CheckStatus(c, err, log.NotSavedFile)

	return file.Filename
}

func Unzip(c *fiber.Ctx, directory string, filename string) {
	r, err := zip.OpenReader(directory + filename)
	log.CheckStatus(c, err, log.NotOpenZIP)
	defer r.Close()

	for _, f := range r.File {
		filePath := filepath.Join(directory, f.Name)

		relPath, err := filepath.Rel(filePath, directory)
		log.CheckStatus(c, err, log.NotRelativePath)

		if !filepath.IsAbs(relPath) && !strings.HasPrefix(relPath, "..") {
			log.SendStatus(c, log.NotSafePath)
		}

		if f.FileInfo().IsDir() {
			err = os.Mkdir(filePath, os.ModePerm)
			log.CheckStatus(c, err, log.NotCreatedDirectory)
			continue
		}

		err = os.MkdirAll(filepath.Dir(filePath), os.ModePerm)
		log.CheckStatus(c, err, log.NotCreatedDirectory)

		outFile, err := os.OpenFile(filePath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, f.Mode())
		log.CheckStatus(c, err, log.NotOpenFile)
		defer outFile.Close()

		rc, err := f.Open()
		log.CheckStatus(c, err, log.NotOpenFile)
		defer rc.Close()

		_, err = io.Copy(outFile, rc)
		log.CheckStatus(c, err, log.NotCopyFile)
	}
}
