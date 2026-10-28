-- Render ```mermaid code blocks to PNG via mermaid-cli (mmdc), cached by content hash.
local outdir = "build/diagrams"
local mmdc = os.getenv("MMDC") or "mmdc"
local pconf = os.getenv("PUPPETEER_CONFIG") or "scripts/puppeteer.json"
os.execute("mkdir -p " .. outdir)

local function exists(p) local f = io.open(p, "r"); if f then f:close(); return true end; return false end

function CodeBlock(el)
  if not el.classes:includes("mermaid") then return nil end
  local hash = pandoc.sha1(el.text)
  local png = outdir .. "/" .. hash .. ".png"
  if not exists(png) then
    local src = outdir .. "/" .. hash .. ".mmd"
    local f = io.open(src, "w"); f:write(el.text); f:close()
    local cfg = exists(pconf) and (" -p " .. pconf) or ""
    local ok = os.execute(mmdc .. cfg .. " -q -b white -i " .. src .. " -o " .. png)
    if not ok or not exists(png) then
      error("Mermaid render failed for " .. src .. "; fix the diagram before publishing")
    end
  end
  local caption = el.attributes["caption"] or ""
  return pandoc.Para({ pandoc.Image(caption, png, "", pandoc.Attr("", {}, {})) })
end
