local M = {}

local function script_path()
	local source = debug.getinfo(1, "S").source
	local dir = vim.fn.fnamemodify(source:sub(2), ":p:h:h")
	return dir .. "/python/main.py"
end

vim.api.nvim_create_user_command("GPTCoding", function(opts)
	local input_text = opts.args or ""
	if input_text == "" then
		vim.notify("GPTCoding: No input provided.", vim.log.levels.WARN)
		return
	end

	local py_script = script_path()
	local cmd = { "python3", py_script, input_text }

	print("Running:", table.concat(cmd, " "))

	local full_output = {} -- collect all strings in answer

	vim.fn.jobstart(cmd, {
		stdout_buffered = true,
		stderr_buffered = true,

		on_stdout = vim.schedule_wrap(function(_, data)
			if not data then
				return
			end
			local lines = vim.tbl_filter(function(l)
				return l and l ~= ""
			end, data)
			for _, line in ipairs(lines) do
				table.insert(full_output, line)
			end
		end),

		on_stderr = vim.schedule_wrap(function(_, data)
			if not data then
				return
			end
			local lines = vim.tbl_filter(function(l)
				return l and l ~= ""
			end, data)
			if #lines > 0 then
				vim.notify(table.concat(lines, "\n"), vim.log.levels.ERROR, { title = "GPTCoding (stderr)" })
			end
		end),

		on_exit = vim.schedule_wrap(function(_, code, _)
			if code ~= 0 then
				vim.notify(
					string.format("Python exited with code %d", code),
					vim.log.levels.ERROR,
					{ title = "GPTCoding" }
				)
				return
			end

			-- print all collected stdout into :messages
			if #full_output > 0 then
				vim.api.nvim_out_write(table.concat(full_output, "\n") .. "\n")
				vim.notify("Answer saved in :messages", vim.log.levels.INFO, { title = "GPTCoding" })
			end
		end),
	})
end, {
	nargs = "+",
	desc = "Send prompt to g4f (gpt-4o) and show answer",
})

return M
