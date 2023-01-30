const moneyFormatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  });

let priceTags = dqa(".currency")

for (let price of priceTags) {
    let content = price.textContent
    price.textContent = moneyFormatter.format(content)
}