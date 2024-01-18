export default function (value) {
  let phone
  if (value) {
    phone = `${value.replace(/\D/g, '').match(/\d+/)}`
    return `8 (${phone.slice(1, 4)}) ${phone.slice(4, 7)}-${phone.slice(7, 9)}-${phone.slice(9, 11)}`
  }
  return ''
}
