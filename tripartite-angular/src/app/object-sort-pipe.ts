// A custom pipe that used to sort iterables
// such as the tenant student list on the class
// creation and edit views
import { Pipe, PipeTransform } from "@angular/core";

@Pipe({ name: 'ObjSortPipe', pure: false })
export class ObjSortPipe implements PipeTransform {
   transform(arr:any, param:any): Array<any> { 
       arr.sort((a:any, b:any) => (a[param] > b[param] ? 1: -1));
       return arr
    }
} 