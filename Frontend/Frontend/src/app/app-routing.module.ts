import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { jwtAuthGuard } from './Guard/jwt-auth.guard';
import { MybookingsComponent } from './Pages/dashboard/Components/mybookings/mybookings.component';
import { DashboardComponent } from './Pages/dashboard/dashboard.component';
import { LoginComponent } from './Pages/login/login.component';
import { RegisterComponent } from './Pages/register/register.component';

const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [jwtAuthGuard] },
  { path: 'mybookings', component: MybookingsComponent,canActivate: [jwtAuthGuard]  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: []
})
export class AppRoutingModule {}
