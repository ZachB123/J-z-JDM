
form = dq("#searchForm")
dq(".search-button").addEventListener("click", () => {
    form.submit()
})