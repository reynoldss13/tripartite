// A custom pipe, transforms the Object into an interable array 
// of the nested values and returns it. Used in conjunction with
// ngFor for nested objects
import { Pipe, PipeTransform } from "@angular/core";

@Pipe({ name: 'ObjTForm', pure: false })
export class ObjTForm implements PipeTransform {
    transform(obj:Object): Array<any> { return Object.values(obj); }
}