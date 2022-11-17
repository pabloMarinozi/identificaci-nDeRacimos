library(readr)
library(stringr)
library(purrr)
library(dplyr)
library(tidyr)
library(TAF)

#####ARGUMENTS
args=commandArgs(trailingOnly = TRUE)
direc = args[1]
modn = as.integer(args[2])
#####FUNCTIONS
get_last <- function(list){ list %>%  tail(n=1)}
get_folder <- function(path){
  path %>% str_split("/") %>% map(head,-1) %>% unlist() %>%  str_c(collapse='/')
}
get_frame_index <- function(names){
  #extracts the index of the frame from its name
  #VID_20220217_101110_0.png returns 0
  #VID_20220217_101110_1.png returns 1
  names %>% str_split("_") %>%
    map(get_last) %>% str_replace(".png","")
}
get_image_df <- function(n, names, df){
  #creates 4 columns for each image_name
  df %>% filter(image_name == names[n+1]) %>%
    select(track_id, label,image_name,x,y,r) %>% 
    rename("image_name_{{n}}":= image_name,
           "x_{{n}}":=x,"y_{{n}}":=y,"r_{{n}}":=r)
}

get_bundles_csv <- function(name,mod){
  dir <- get_folder(name)
  df <- read_csv(name) %>% 
    mutate(frame_index = image_name %>% get_frame_index() %>% as.integer()) %>%
    filter(detection == "Detecting",frame_index %% mod == 0) 
  image_names <- df$image_name %>% unique()
  mkdir(paste0(dir,"/mod",mod))
  
  0:(length(image_names)-1) %>%
    map(get_image_df,image_names,df) %>% 
    reduce(full_join) %>% mutate(nro_kf = length(image_names)) %>% 
    relocate(nro_kf, .after = label) %>% 
    write_csv(paste0(dir,"/mod",mod,"/bundles.csv"),na = "NULL")
}

get_bundles_csv_pairs <- function(name,mod){
  dir <- get_folder(name)
  df <- read_csv(name) %>% 
    mutate(frame_index = image_name %>% get_frame_index() %>% as.integer()) %>%
    filter(detection == "Detecting",frame_index %% mod == 0) 
  image_names <- df$image_name %>% unique()
  mkdir(paste0(dir,"/mod",mod))
  
  0:(length(image_names)-1) %>%
    map(get_image_df,image_names,df) %>% 
    reduce(full_join) %>% mutate(nro_kf = length(image_names)) %>% 
    relocate(nro_kf, .after = label) %>% 
    write_csv(paste0(dir,"/mod",mod,"/bundles.csv"),na = "NULL")
}

name <- direc
mod <- c(modn)
crossing(name,mod) %>% pmap(get_bundles_csv)
