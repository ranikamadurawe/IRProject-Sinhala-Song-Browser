import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'removeSymbol'
})
export class RemoveSymbolPipe implements PipeTransform {

  transform(value: any, ...args: any[]): any {
    let ret_val = value.replace(/—|\//gi, "")
    let ret_val_no_line = ret_val.replace(/\n{2,}/gi, "")
    console.log(ret_val_no_line)
    return ret_val_no_line;
  }

}
