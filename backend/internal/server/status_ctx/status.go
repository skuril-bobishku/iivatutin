package status_ctx

/*func SendStatus(c *fiber.Ctx, status func() (int, fiber.Map)) {
	statusCode, statusJSON := status()
	c.Status(statusCode).JSON(statusJSON)
	c.Context().Done()
}

func CheckStatus(c *fiber.Ctx, err error, status func() (int, fiber.Map)) {
	if err != nil {
		SendStatus(c, status)
	}
}*/
