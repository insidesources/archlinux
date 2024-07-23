require("config.lazy")
require("lazy").setup("plugins")
vim.cmd("colorscheme onedark")
-- bufferline
vim.opt.termguicolors = true
require("bufferline").setup{}
