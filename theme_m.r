# Reference
# 	componentsにelementsを代入することでスタイルは決まる
# 	https://ggplot2.tidyverse.org/reference/theme.html
# 	https://ggplot2.tidyverse.org/reference/element.html
#
# Usage
# 	g <- g + theme_m()
# 	g <- g + 
# 	  scale_x_continuous(sec.axis = dup_axis()) +
# 	  scale_y_continuous(sec.axis = dup_axis())

theme_m <- function() {
	text_size <- 14
	return(
		theme_linedraw() +
		theme(
			# Inward axis(t,b,l,r)
			axis.ticks.length = unit(-0.25, "cm"), 
  			axis.text.x.bottom = element_text(size = text_size, margin = margin(t = 0.35, unit = "cm")),
  			axis.text.y.left = element_text(size = text_size, margin = margin(r = 0.35, unit = "cm")),
			
			# Remove secondary axis label
  			axis.text.x.top = element_text(size = 0, margin = margin(b = 0.35, unit = "cm")),
  			axis.text.y.right = element_text(size = 0, margin = margin(l = 0.35, unit = "cm")),

			# Vivid axis 
			axis.line = element_line(size = 0.5),
			axis.ticks = element_line(size = 0.5),

			# ==============================
	
			# Legend text
			legend.text = element_text(size = text_size),
			legend.title = element_blank(),

			# Legend float position
			legend.position = c(.00, .95),
			legend.justification = c("left", "top"),
			legend.box.just = "top",
			legend.margin = margin(6, 6, 6, 6),
			legend.box = "horizontal",
			
			# Legened color(white + frame)
  			# legend.background = element_rect(fill="white", size=0.5, linetype="solid", colour="black"),

			# Legened color(transparent)
  			legend.background = element_rect(colour = "transparent", fill = NA),

			# ==============================

			# Remove grid line (optional)
  			# panel.grid = element_blank(),

			# grid line
  			panel.grid = element_line(size = 3, color = "gray"),
  			panel.grid.minor = element_blank(),

			# ==============================

			# Remove secondary axis title
			axis.title.x.top = element_blank(), 
			axis.title.y.right = element_blank(),


		)
	)
}