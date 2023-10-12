import { Component, Input } from '@angular/core';
import { Booking } from 'src/app/Entities/Booking';

@Component({
  selector: 'app-booking-box',
  templateUrl: './booking-box.component.html',
  styleUrls: ['./booking-box.component.css']
})
export class BookingBoxComponent {
  @Input()
  booking : Booking| undefined;

  formatDate(dateString: string|undefined): Date {

    return new Date(dateString?dateString:"");
  }
}
