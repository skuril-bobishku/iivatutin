package config

import (
	"github.com/joho/godotenv"
	"os"
	"strconv"
)

func SetServerDomain() string {
	err := godotenv.Load(".env")

	if err != nil {
		panic(err)
	}

	return os.Getenv("SERVER_DOMAIN")
}

func SetServerPort() string {
	err := godotenv.Load(".env")

	if err != nil {
		panic(err)
	}

	return os.Getenv("SERVER_PORT")
}

func GetServerDirectory() string {
	err := godotenv.Load(".env")

	if err != nil {
		panic(err)
	}

	return os.Getenv("FILE_DIRECTORY")
}

func GetMaxImagesCount() int {
	err := godotenv.Load(".env")

	if err != nil {
		panic(err)
	}

	temp := os.Getenv("MAX_PARSE_IMAGE_COUNT")
	count, err := strconv.Atoi(temp)
	if err != nil {
		panic(err)
	}

	return count
}
