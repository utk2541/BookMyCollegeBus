import { Component } from '@angular/core';
import { User } from 'src/app/Entities/User';
import { Router } from '@angular/router';
import { HttpQueryService } from 'src/app/Services/http-query.service';
import { LocalStorageService } from 'src/app/Services/local-storage-service.service';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  user: User = {
    username: '',
    password: '',
  };
  alertMessage: string | undefined;
  submit(): void {
    this.http.login(this.user).subscribe({
      next: (ob) => {
        this.lc.setItem('jwt', ob.body.jwt);
        this.router.navigate(['/dashboard']);
      },
      error: (error) => {
        if (error.error.message)
          (this.alertMessage = error.error.message),
            setInterval(() => (this.alertMessage = undefined), 4000);
        else this.alertMessage = 'Unkown Error';
      },
    });

    this.user = {
      username: '',
      password: '',
    };
  }

  toRegister(): void {
    this.router.navigate(['/register']);
  }
  constructor(
    private router: Router,
    private http: HttpQueryService,
    private lc: LocalStorageService
  ) {}
}
