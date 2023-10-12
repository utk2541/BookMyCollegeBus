import { provideCloudinaryLoader } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Booking } from 'src/app/Entities/Booking';
import { Schedule } from 'src/app/Entities/Schedule';
import { HttpQueryService } from 'src/app/Services/http-query.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
})
export class DashboardComponent implements OnInit {
  schedules: Schedule[] | null = [];

  ngOnInit(): void {
    this.http.getSchedule(true).subscribe({
      next: (obj) => {
        this.schedules = obj.body;

        console.log(this.schedules);
      },
      error: (error) => {
        console.log(error.error);
      },
    });
    setInterval(() => {
      this.http.getSchedule(false).subscribe({
        next: (obj) => {
          this.schedules = obj.body;

          console.log(this.schedules);
        },
        error: (error) => {
          console.log(error.error);
        },
      });
    }, 10 * 60 * 1000);

    setInterval(() => {
      this.prune();
    }, 1000);
  }
  private prune(): void {
    while (
      this.schedules !== undefined &&
      this.schedules?.length &&
      Date.parse(this.schedules[0].BookingEnd) < Date.now()
    ) {
      console.log(this.schedules.shift());
    }
  }

  handleBook(booking: Schedule) {
    this.http.book(booking).subscribe({
      next: (obj) => (alert(obj.body),this.http.getSchedule(false)),
      error: (error) => {
        console.log(error.error);
      },
    });
  }
  constructor(private http: HttpQueryService) {}
}
