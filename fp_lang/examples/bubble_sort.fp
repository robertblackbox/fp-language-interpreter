// Bubble Sort implementation in FP Language

// Helper function to perform one pass of bubble sort
// Returns a tuple (sorted_list, swapped) where swapped indicates if any swaps were made
def bubblePass(lst) = 
    if length(lst) < 2 then 
        (lst, false)
    else {
        let first = head(lst)
        let rest = tail(lst)
        let (sorted_rest, swapped) = bubblePass(rest)
        let next = head(sorted_rest)
        
        if first > next then
            ([next] + [first] + tail(sorted_rest), true)
        else
            ([first] + sorted_rest, swapped)
    }

// Main bubble sort function that repeatedly calls bubblePass until no swaps are needed
def bubbleSort(lst) = {
    let (new_lst, swapped) = bubblePass(lst)
    if swapped then
        bubbleSort(new_lst)
    else
        new_lst
}

// Test the bubble sort implementation
let test_list = [64, 34, 25, 12, 22, 11, 90]
let result = bubbleSort(test_list)
result  // Should print [11, 12, 22, 25, 34, 64, 90]
