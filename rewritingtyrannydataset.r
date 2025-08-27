library(tidyverse)
library(stringr)
library(dplyr)

df <- read.csv("C:/Users/anton/Desktop/alltyranny.csv")
df <- df[, c("aka", "date", "description", "location_city", "location_state","publication_frequency")]

df <- df %>%
    mutate(page_number = as.integer(str_extract(aka, "(?<=\\?sp=)\\d+")))
# I know that last part of url is the page number so making a column for page number

#ai helped write the function below
extract_snippets <- function(text, window = 5) {
    # Split into words
    words <- unlist(str_split(text, "\\s+"))

    # Find indices of "tyranny" (case insensitive)
    idx <- which(str_detect(tolower(words), "\\btyranny\\b"))

    if (length(idx) == 0) {
        return(NULL)
    }

 
    snippets <- sapply(idx, function(i) {
        start <- max(1, i - window)
        end <- min(length(words), i + window)
        paste(words[start:end], collapse = " ")
    })

    return(snippets)
}

df_snippets <- df %>%
    rowwise() %>%
    mutate(snippets = list(extract_snippets(description))) %>%
    unnest(snippets) %>%
    mutate(description = snippets) %>% 
    select(-snippets)
  

colnames(df_snippets) <- c("id", "pub_date", "text", "city", "state", "frequency", "page_number")


write.csv(df_snippets, "C:/Users/anton/Desktop/alltyrannysimplified.csv")
