# Create a function that handles the fact that the list of activities are of unequal length. It must be done because data frame columns must be lists of equal lengths

convert_list_to_tbl <- function(activities) {
  tryCatch({
    as.data.frame(t(unlist(activities)), stringsAsFactors = FALSE)
  }, error = function(e) {
    NA
  })
}
