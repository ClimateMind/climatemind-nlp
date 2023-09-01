
#'
#'
#'cc: climate concept
#'    each climate concept has 4 dimensions (change_direction, type_of, base, aspect_changing)
#'

library(jsonlite)
library(tidyverse)


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


## work on topics --------------------------------------------------------------
cc_base <- cc_df %>%
  dplyr::distinct(name_base) %>%
  arrange(name_base)

## save as csv file for manual classification
readr::write_csv(x = cc_base, file = 'cc_base.csv')


## read in classified topics ---------------------------------------------------
