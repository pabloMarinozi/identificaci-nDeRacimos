library(readr)
library(dplyr)
library(stringr)
library(purrr)
setwd("../input/nubes_completas/bonarda/frames03")

#lee el archivo de reconstrucciones
df <- read_csv("keypoints_positions_volumes.csv")

df_val <- df %>%
  #filtra puntos de validación
  filter(!is.na(d2val1) | !is.na(d2val2)) %>% 
  #calcula la distancia de validación de cada imagen
  group_by(img_name) %>% 
  summarise(val1_mean = mean(d2val1,na.rm=TRUE),
            val2_mean = mean(d2val2,na.rm=TRUE)) %>% 
  # filtra con un threshold de 4 milímetros
  filter(abs(val1_mean-2) < 0.4 & abs(val1_mean-2) < 0.4)


df_val$img_name <- df_val$img_name %>%
  str_replace("_F0.png", "") %>%
  str_replace("_F-1.png", "") %>% 
  str_replace("_F3.png", "") %>% paste0(".ply")


buenas <- df_val %>% select(img_name) %>% unique()

buenas %>% write_csv("buenas.csv")

#tibble(index = index_buenas, name = name_buenas) %>% write_csv("nubes_buenas_bonarda.csv") 

