return {
    'nvim-lualine/lualine.nvim',
    dependencies = { 'nvim-tree/nvim-web-devicons' },
    config = function()
	    require('lualine').setup({
	    options = {
		    theme = 'onedark',
		    section_separators = { left = '', right = '' },
  		    component_separators = { left = '', right = '' }
	    },
	      sections = {
    			lualine_a = {'mode'},
    			lualine_b = {'branch', 'diff', 'diagnostics'},
    			lualine_c = {'filename'},
    			lualine_x = {'filetype'},
    			lualine_y = {''},
    			lualine_z = {
    					{ 'datetime',
					-- options: default, us, uk, iso, or your own format string ("%H:%M", etc..)
					style = '%A, %B %d %Y %l:%M%p' }
  					}
  				},
    			})
    		end
	}
