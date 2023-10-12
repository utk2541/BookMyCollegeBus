import { Component } from '@angular/core';
import { User } from 'src/app/Entities/User';
import { HttpQueryService } from 'src/app/Services/http-query.service';
import { Router } from '@angular/router';
@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  user: User = {
    username: '',
    password: '',
  };
  alertMessage: string | undefined;
  constructor(private http: HttpQueryService,private router: Router) {}
  submit(): void {
    console.log(this.user);

    this.http.register(this.user).subscribe({
      next: () => {
        this.router.navigate(['/login']);
      },
      error: (error) => {
        console.log(error.error)
        if (error.error.username)
          (this.alertMessage = error.error.username[0]),
            setInterval(() => (this.alertMessage = undefined), 4000);
        else this.alertMessage = 'Unkown Error';
      },
    });

    this.user = {
      username: '',
      password: '',
    };
  }
}
