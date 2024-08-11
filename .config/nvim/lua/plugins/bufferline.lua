return {'akinsho/bufferline.nvim',
	version = "*",
	dependencies = 'nvim-tree/nvim-web-devicons',
	config = function()
		require("bufferline").setup({
			options = {
				buffer_close_icon = "⨉",
				modified_icon = "●",
				close_icon = "⨉",
				show_buffer_icons = true,
				show_buffer_close_icons = true,
				show_close_icon = true,
				show_tab_indicators = true,
				separator_style = "thin",
				indicator = {
					style = 'none',
				},
			},
	        })
            end
       }
