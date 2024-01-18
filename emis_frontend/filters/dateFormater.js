import {convertDateFormat} from "@/utils";

export default function (value, format, sourceFormat='yyyy-MM-dd'){
  if (!format ){
    return value
  }
  return convertDateFormat(value, sourceFormat, format)
}
