import { CanActivateFn } from '@angular/router';
import { Router } from '@angular/router';

export const jwtAuthGuard: CanActivateFn = (route, state) => {
  
  const token = localStorage.getItem('jwt');

  if (token) {
    return true; 
  } else {
    const router = new Router();
  
    return router.navigateByUrl("/login");
  }
};
