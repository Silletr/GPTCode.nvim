local M = {}

function M.run(first, ...)
	local args = { ... }
	print("First:", first)
	print("Args:", vim.inspect(args))
end

vim.api.nvim_create_user_command("GPTCoding", function(opts)
	local input_text = opts.args
	print("Entered:", input_text)

	vim.fn.jobstart({ "python3", "lua/GPTCodeNvim/python/main.py", input_text }, {
		stdout_buffered = true,
		on_stdout = function(_, data, _)
			if data then
				local filtered = {}
				for _, line in ipairs(data) do
					if line ~= "" then
						table.insert(filtered, line)
					end
				end
				print("Python output:", table.concat(filtered, "\n"))
			end
		end,
		on_stderr = function(_, data, _)
			if data then
				print("Python error:", table.concat(data, "\n"))
			end
		end,
	})
end, { nargs = "+", desc = "Send text to Python" })

return M
