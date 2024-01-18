export default function (value, key) {
  if (value) {
    const data = []
    value.forEach(item => {
      data.push(item[key])
    })
    return data.join(', ')
  }
  return null
}
