import { Component, OnInit } from '@angular/core';
import { Booking } from 'src/app/Entities/Booking';
import { HttpQueryService } from 'src/app/Services/http-query.service';

@Component({
  selector: 'app-mybookings',
  templateUrl: './mybookings.component.html',
  styleUrls: ['./mybookings.component.css'],
})
export class MybookingsComponent implements OnInit {
  bookings: Booking[] = [];
  constructor(private http: HttpQueryService) {}
  ngOnInit(): void {
    this.http.getBookings().subscribe({
      next: (obj) => {
        this.bookings= obj.body;
        
        console.log(this.bookings)
      },
      error: (error) => {
        console.log(error.error);
      },
  })
  }
}
