package config

import (
	"github.com/joho/godotenv"
	"os"
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
