package server

import (
	"fmt"
	"github.com/gofiber/fiber/v2"
	"github.com/klauspost/compress/zip"
	stc "github.com/skuril-bobishku/iivatutin/backend/internal/server/status_ctx"
	"golang.org/x/text/encoding/charmap"
	"io"
	"os"
	"path/filepath"
	"strings"
)

func saveFile(c *fiber.Ctx, directory string, extension string) func() (int, fiber.Map) {
	file, err := c.FormFile("file")
	if err != nil {
		return stc.NotRequired
	}

	if filepath.Ext(file.Filename) != extension {
		return stc.BadFileFormat
	}

	_, err = os.Stat(directory)
	if os.IsNotExist(err) {
		err = os.MkdirAll(directory, os.ModePerm)
		if err != nil {
			return stc.NotCreatedDirectory
		}
	}

	err = c.SaveFile(file, directory+file.Filename)
	if err != nil {
		return stc.NotSavedFile
	}

	return func() (int, fiber.Map) {
		return stc.FileSaved(file.Filename)
	}
}

func unzip(c *fiber.Ctx, directory string, fullname string) func() (int, fiber.Map) {
	fileExt := filepath.Ext(fullname)
	fileName := strings.TrimSuffix(fullname, fileExt)

	r, err := zip.OpenReader(directory + fullname)
	if err != nil {
		return stc.NotOpenZIP
	}
	defer r.Close()

	directory = filepath.Join(directory, fileName)

	for _, f := range r.File {
		if f.NonUTF8 {
			//f.Name = fileName
			decoder := charmap.CodePage866.NewDecoder()
			decodedName, err := decoder.String(f.Name)
			if err != nil {
				fmt.Println("Ошибка декодирования:", err)
			}

			f.Name = decodedName
		}

		filePath := filepath.Join(directory, f.Name)

		relPath, err := filepath.Rel(filePath, directory)
		if err != nil {
			return stc.NotRelativePath
		}

		if !filepath.IsAbs(relPath) && !strings.HasPrefix(relPath, "..") {
			return stc.NotSafePath
		}

		if f.FileInfo().IsDir() {
			err = os.MkdirAll(filepath.Dir(filePath), os.ModePerm)
			if err != nil {
				return stc.NotCreatedDirectory
			}
			continue
		}

		err = os.MkdirAll(filepath.Dir(filePath), os.ModePerm)
		if err != nil {
			return stc.NotCreatedDirectory
		}

		rc, err := f.Open()
		if err != nil {
			return stc.NotOpenFile
		}
		defer rc.Close()

		outFile, err := os.Create(filePath)
		if err != nil {
			return stc.NotCreateFile
		}
		defer outFile.Close()

		_, err = io.Copy(outFile, rc)
		if err != nil {
			return stc.NotCopyFile
		}
	}

	return func() (int, fiber.Map) {
		return stc.FileUnzip(filepath.Join(directory, fullname))
	}
}
