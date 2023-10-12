import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import {HttpClientModule} from '@angular/common/http'
import { HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './Pages/login/login.component';
import { RegisterComponent } from './Pages/register/register.component';
import { DashboardComponent } from './Pages/dashboard/dashboard.component';
import { HeaderComponent } from './Pages/dashboard/Components/header/header.component';
import { DashboardBoxComponent } from './Pages/dashboard/Components/dashboard-box/dashboard-box.component';
import { BookingBoxComponent } from './Pages/dashboard/Components/booking-box/booking-box.component';
import { MybookingsComponent } from './Pages/dashboard/Components/mybookings/mybookings.component';
import { HttpQueryService } from './Services/http-query.service';
import { AlertComponent } from './Components/alert/alert.component';
import { LocalStorageService } from './Services/local-storage-service.service';
import { AuthInterceptorService } from './Services/auth-interceptor.service';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    DashboardComponent,
    HeaderComponent,
    DashboardBoxComponent,
    BookingBoxComponent,
    MybookingsComponent,
    AlertComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [HttpQueryService,LocalStorageService,{
    provide: HTTP_INTERCEPTORS,
    useClass: AuthInterceptorService,
    multi: true,
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
