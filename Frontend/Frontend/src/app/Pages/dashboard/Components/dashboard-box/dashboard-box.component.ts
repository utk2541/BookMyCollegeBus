import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Schedule } from 'src/app/Entities/Schedule';

@Component({
  selector: 'app-dashboard-box',
  templateUrl: './dashboard-box.component.html',
  styleUrls: ['./dashboard-box.component.css'],
})
export class DashboardBoxComponent {
  @Input()
  schedule: Schedule | undefined;

  @Output()
  onBook: EventEmitter<Schedule> = new EventEmitter<Schedule>();


  formatDate(dateString: string | undefined): Date {
    return new Date(dateString ? dateString : '');
  }

  book(): void {
    this.onBook.emit(this.schedule);
  }
}
