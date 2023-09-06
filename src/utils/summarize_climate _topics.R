
#'
#'
#'cc: climate concept
#'    each climate concept has 4 dimensions (change_direction, type_of, base, aspect_changing)
#'

library(jsonlite)
library(tidyverse)
library(googlesheets4)


## read in the node data in json format ----------------------------------------

js_url <- "https://www.project-c-test-backend.de/climate-concept-nodes"
cc <- jsonlite::fromJSON(txt = js_url)

cc_df <- as.data.frame(cc$data) %>%
  tidyr::separate(name, into = c("name_dirc", "name_type", "name_base", "name_aspe"),
                  sep = "_", remove = F) %>%
  as.data.frame()

## make sure if the `id` and `_id` is unique keys -- Yes!
nrow(cc_df) == unique(cc_df$`id`) %>% length()
nrow(cc_df) == unique(cc_df$`_id`) %>% length()


cc_df_ <- cc_df %>%
  dplyr::mutate(name_type = gsub('[[:punct:] ]+', ' ', name_type),
                name_type = str_squish(name_type)) %>%
  dplyr::select(starts_with('name_')) %>%
  dplyr::distinct(name_type, name_base, .keep_all = T) %>%
  dplyr::mutate(name_type_base = paste(name_type, name_base, sep = '_')) %>%
  as.data.frame()



## work on topics --------------------------------------------------------------
cc_base <- cc_df_ %>%
  dplyr::distinct(name_base) %>%
  arrange(name_base)

## save as csv file for manual classification
getwd()
readr::write_csv(x = cc_base, file = './src/utils/climate_topics/cc_base.csv')


## read in classified topics ---------------------------------------------------
gsheet <- "https://docs.google.com/spreadsheets/d/1UYCkbB_6eQlA5z9nDeSHsmTQGVTeg6wJd_uRO1oGv4g/edit?usp=sharing"
topic <- googlesheets4::read_sheet(ss = gsheet) %>%
  # dplyr::mutate(topic_tier1 = ifelse(topic_tier1=='?', 'Other', topic_tier1)) %>%
  as.data.frame()


###' add other information to decide the 'topic'
###' - revise the topic in gsheet if necessary
cc_df_t <- cc_df_ %>%
  left_join(., topic, by = 'name_base')

###' join the topic classification data to the original df
cc_df_topic <- cc_df %>%
  left_join(., topic, by = 'name_base') %>%
  dplyr::select(-starts_with('name_'))

cat('\n Total # of topics:', length(unique(cc_df_topic$topic_tier1)), '\n\n')


## save the result
readr::write_csv(x = cc_df_topic, file = './src/utils/climate_topics/cc_df_topic.csv')

