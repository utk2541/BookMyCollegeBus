import { Injectable } from '@angular/core';
import {
  HttpClient,
  HttpErrorResponse,
  HttpHeaders,
} from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Observable, throwError, tap, of } from 'rxjs';
import { User } from '../Entities/User';
import { catchError } from 'rxjs/operators';
import { Booking } from '../Entities/Booking';
import { Schedule } from '../Entities/Schedule';
const options = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json',
  }),
  observe: 'response' as const,
};
@Injectable({
  providedIn: 'root',
})
export class HttpQueryService {
  private apiUrl = environment.apiUrl;
  constructor(private http: HttpClient) {}
  private cachedData: any | undefined;
  login(user: User): Observable<any> {
    return this.http.post<User>(this.apiUrl + 'user/login', user, options).pipe(
      catchError((error) => {
        return throwError(() => new HttpErrorResponse(error));
      })
    );
  }
  register(user: User): Observable<any> {
    return this.http
      .post<User>(this.apiUrl + 'user/registration', user, options)
      .pipe(
        catchError((error) => {
          return throwError(() => new HttpErrorResponse(error));
        })
      );
  }

  getSchedule(cacheAllowed: boolean): Observable<any> {
    if (this.cachedData && cacheAllowed) return of(this.cachedData);

    return this.http.get(this.apiUrl + 'app/currentBus', options).pipe(
      tap((data) => {
        this.cachedData = data;
      }),
      catchError((error) => {
        return throwError(() => new HttpErrorResponse(error));
      })
    );
  }
  getBookings(): Observable<any> {
    return this.http.get(this.apiUrl + 'app/userBookings', options).pipe(
      catchError((error) => {
        return throwError(() => new HttpErrorResponse(error));
      })
    );
  }

  book(booking: Schedule): Observable<any> {
  
    return this.http.post<Schedule>(this.apiUrl + 'app/bookSeat', booking, options).pipe(
      catchError((error) => {
        return throwError(() => new HttpErrorResponse(error));
      })
    );
  }
}
