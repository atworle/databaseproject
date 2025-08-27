
library(jsonlite)
library(httr)
library(tidyverse)

pages <- 1:4
newurl <- vector("list", length(pages))


for(i in seq_along(pages)){
    p <- pages[i]
  newurl[[i]] <- paste0(
   "https://www.loc.gov/collections/chronicling-america/?c=160&dl=page&end_date=1783-12-31&ops=AND&qs=tyranny&searchType=advanced&sp=", p, "&start_date=1736-09-03&fo=json"
)
}

results <- vector("list", length(newurl))
for (i in seq_along(newurl)) {
    json_stuff <- GET(newurl[[i]])
    if (json_stuff$status_code == 200) {
        # only pulling json info if successful status code of 200
        results[[i]] <- content(json_stuff, "text")
        # ensures I don't overlap the api
    } else {
        results[[i]] <- NULL
        # making bad results NULL
    }
    Sys.sleep(3)
    # pauses whether or not there is failure to ensure I don't overload api
}

# this removes null results from the list I made so the json data can be organized
# the new null results i believe were large pictures on pages or something like that based on cursory debugging
organized_json <- list()
# turning my results into a list
for (i in 1:length(results)) {
    json_data <- fromJSON(results[[i]])
    organized_json[[i]] <- json_data$results
}

df <- bind_rows(organized_json)



df_clean <- df %>% mutate(across(where(is.list), ~ sapply(.x, function(x) {
    if (length(x) == 0) {
        return("")
    } else {
        paste(x, collapse = "; ")
    }
})))



write.csv(df_clean, "C:/Users/anton/Desktop/alltyranny.csv", row.names = FALSE)