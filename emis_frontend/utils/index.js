import { format, parse } from 'date-fns'

const toLower = text => {
    if (text !== null){
        return text.toString().toLowerCase()
    }
    return ''
}

export function convertDateFormat(item, formatStart, formatEnd) {
  if (item) {
    return format(parse(item, formatStart, new Date()), formatEnd)
  } else {
    return item
  }
}

export const periodValidator = (value) => {
  const VRegExp = value.search(/^(0[1-9]|1[0-2])\.(20[2-9][0-9]|203[0-9])$/);
  if (VRegExp === 0) {
    return {type: 'success', message: null}
  }
  return {type: 'error', message: 'Ошибка формата периода: (ММ.ГГГГ)'}
}

const utils = {
    searchByFields(items, searchedItems, term, searchField) {
        if (term || typeof term === 'boolean') {
            let result;
            for (let i = 0; i < searchField.length; i++) {
                if (typeof term === 'boolean') {
                    result = searchedItems.filter(item => item[searchField[i]] === term);
                    if (result.length === 0) {
                        result = items.filter(item => item[searchField[i]] === term);
                    }
                } else {
                    result = searchedItems.filter(item => toLower(item[searchField[i]]).includes(toLower(term)));
                    if (result.length === 0) {
                        result = items.filter(item => toLower(item[searchField[i]]).includes(toLower(term)));
                    }
                }
                if (result.length === 0) {
                    continue;
                }
                return result;
            }
            return []
        }
        return items
    },
    getParamsUrl(url, key){
      url = new URL(url)
      return url.searchParams.get(key)
    }
}
export default utils
