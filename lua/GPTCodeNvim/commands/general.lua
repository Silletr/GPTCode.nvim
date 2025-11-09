local function M(first, ...)
	local args = { ... }
	print("First:", first)
	print("Args:", vim.inspect(args))
end

-- регистрация команды
vim.api.nvim_create_user_command("GPTCoding", function(opts)
	M("command", opts.fargs)
	vim.notify("GPTCoding executed!", vim.log.levels.INFO)
end, { nargs = "+", desc = "Test command for plugin" })
