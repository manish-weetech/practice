// =============================================
// DSA Practice File
// Run: node practice.js
// =============================================

const prompt = require("prompt-sync")();

//  recursion

// ---- Your Code Below ----

// function palindrome(number) {
//   let copy = number;
//   let ans = 0;
//   while (number > 0) {
//     let digit = number % 10;
//     ans = ans * 10 + digit;
//     number = Math.floor(number / 10);
//   }
//   if (copy == ans) {
//     return "Is palindrome";
//   } else {
//     return "Not a palindrome";
//   }
// }

// console.log(palindrome(12));

// =========================================

// function armstrong(number) {
//   let count = countNumber(number);
//   // let count = number.toString().length;
//   let ans = 0;
//   while (number > 0) {
//     let digit = number % 10;
//     ans = ans + digit ** count;
//     number = Math.floor(number / 10);
//   }
//   return ans;
// }

// function countNumber(number) {
//   let count = 0;
//   while (number > 0) {
//     number = Math.floor(number / 10);
//     count++;
//   }
//   return count;
// }

// console.log(armstrong(1634));

// ============================================

// function factorial(n) {
//   if (n == 0 || n == 1) {
//     return n;
//   }
//   return n * (n - 1);
// }

// console.log(factorial(3));

// function factorial(n) {
//   let ans = 1;
//   if (n == 0 || n == 1) {
//     return n;
//   }
//   while (n > 0) {
//     ans = ans * n;
//     n = n - 1;
//   }
//   return ans;
// }
// console.log(factorial(1));

// ============================================

// function prime(number) {
//   let isPrime = true;
//   if (number == 0 || number == 1) {
//     return isPrime;
//   }
//   for (let i = 2; i < number; i++) {
//     if (number % i == 0) {
//       isPrime = false;
//     }
//   }
//   return isPrime;
// }

// console.log(prime(6));

// function prime(number) {
//   for (let i = 2; i <= number; i++) {
//     let isPrime = true;
//     for (let j = 2; j < i; j++) {
//       if (i % j === 0) {
//         isPrime = false;
//         break;
//       }
//     }
//     if (isPrime) {
//       console.log(i);
//     }
//   }
// }
// prime(100)

//=======================================

// function sumOfDigits(n) {
//   let sum = 0;
//   while (n > 0) {
//     let digit = n % 10;
//     sum = sum + digit;
//     n = Math.floor(n / 10);
//   }
//   return sum;
// }
// console.log(sumOfDigits(123));

// =======================================

// function ReverseANumber(n) {
//   let ans = 0;
//   while (n > 0) {
//     let digit = n % 10;
//     ans = ans * 10 + digit;
//     n = Math.floor(n / 10);
//   }
//   return ans
// }
// console.log(ReverseANumber(1234));

// =======================================

// 6(1+2+3=6) and 28(1+2+4+7+14=28)
// function perfectNumber(n) {
//   let sum = 0;
//   for (let i = 1; i < n; i++) {
//     if (n % i == 0) {
//       sum = sum + i;
//     }
//   }
//   if (sum == n) {
//     return "perfectNumber";
//   } else {
//     return "not a perfectNumber";
//   }
// }
// console.log(perfectNumber(28));

// =========================================

// function GCD(n1, n2) {
//   let n = Math.min(n1, n2);
//   for (let i = n; i >= 0; i--) {
//     if (n1 % i == 0 && n2 % i == 0) {
//       return i;
//     }
//   }
// }

// console.log(GCD(16,20));

// function GCD(a, b) {
//   if (a == b) {
//     return a;
//   } else if (a > b) {
//     return GCD(a - b, b);
//   } else {
//     return GCD(a, b - a);
//   }
// }
// console.log(GCD(16,20));

// =========================================

// function fibonacciSeries(n) {
//   let a = 0;
//   let b = 1;

//   for (let i = 0; i < n; i++) {
//     console.log(a);
//     let next = a + b;
//     a = b;
//     b = next;
//   }
// }

// fibonacciSeries(10);

//==========================================

// let arr = [2, 4, 5, 7, 2];
// let large = arr[0];
// for (let i = 1; i < arr.length; i++) {
//   if (arr[i] > large) {
//     large = arr[i];
//   }
// }
// console.log(large);

// let arr = [2, 4, 5, 7, 2];
// let smallest = arr[0];
// for (let i = 1; i < arr.length; i++) {
//   if (arr[i] < smallest) {
//     smallest = arr[i];
//   }
// }
// console.log(smallest);

// let arr = [2, 4, 5, 7, 2];
// let large = arr[0];
// let secondLarge = arr[1]
// for (let i = 1; i < arr.length; i++) {
//   if (arr[i] > large) {
//     secondLarge = large;
//     large = arr[i];
//   }
// }
// console.log(large);
// console.log(secondLarge);

// ==========================================

//bubble sort

// let arr = [2, 4, 3, 7, 1];
// let n = arr.length;
// while (n > 0) {
//   let i = 0;
//   while (i < n - 1) {
//     if (arr[i] > arr[i + 1]) {
//       let temp = arr[i];
//       arr[i] = arr[i + 1];
//       arr[i + 1] = temp;
//     }
//     i++
//   }
//   n--
// }
// console.log(arr);

// let arr = [2, 4, 3, 7, 1];

// for (let i = 0; i < arr.length; i++) {
//   for (let j = 0; j < arr.length - 1 - i; j++) {
//     if (arr[j] > arr[j + 1]) {
//       let temp = arr[j];
//       arr[j] = arr[j + 1];
//       arr[j + 1] = temp;
//     }
//   }
// }

// console.log(arr);

// Merge two sorted arrays.

// let arr1 = [1, 2, 3];
// let arr2 = [1, 5, 6];
// let arr = [];
// let i = 0,
//   j = 0,
//   k = 0;
// while (i < arr1.length && j < arr2.length) {
//   if (arr1[i] < arr2[j]) {
//     arr[k] = arr1[i];
//     i++;
//     k++;
//   } else {
//     arr[k] = arr2[j];
//     j++;
//     k++;
//   }
// }

// while (i < arr1.length) {
//   arr[k] = arr1[i];
//   i++;
//   k++;
// }

// while (j < arr2.length) {
//   arr[k] = arr2[j];
//   j++;
//   k++;
// }

// console.log(arr);

// ==================================

// Remove duplicate elements

// let arr = [1, 1, 2, 5, 2, 3];
// let ans = [];
// ans.push(arr[0]);

// for (let i = 1; i < arr.length; i++) {
//   let hasElement = false;
//   for (let j = 0; j < ans.length; j++) {
//     if (arr[i] == ans[j]) {
//       hasElement = true;
//       break;
//     }
//   }
//   if (!hasElement) {
//     ans.push(arr[i]);
//   }
// }

// console.log(ans);

// ===============================================

// Find missing number in an array from 1 to N.

// let arr = [1, 2, 3, 5, 6, 7];
// for (let i = 0; i < arr.length; i++) {
//   if(arr[i]!=i+1){
//     console.log(i+1);
//     break;
//   }
// }

// =====================================

// reverse a array
// function reverse(arr, a, b) {
//   a = 0;
//   b = arr.length-1;
//   while (a < b) {
//     let temp = arr[a];
//     arr[a] = arr[b];
//     arr[b] = temp;
//     a++;
//     b--;
//   }
// }
// reverse(arr);
// console.log(arr);

// =================================

// Rotate an array left by K positions.

// let arr = [1, 2, 3, 5, 6, 7];
// k = 2;
// k = k % arr.length;

// reverse(0, k - 1);
// reverse(k, arr.length - 1);
// reverse(0, arr.length - 1);
// function reverse(a, b) {
//   while (a < b) {
//     let temp = arr[a];
//     arr[a] = arr[b];
//     arr[b] = temp;
//     a++;
//     b--;
//   }
// }
// console.log(arr);

// Rotate an array right by K positions.

// let arr = [1, 2, 3, 5, 6, 7];
// k = 2;
// k = k % arr.length;

// reverse(0, arr.length - 1);
// reverse(0, k - 1);
// reverse(k, arr.length - 1);
// function reverse(a, b) {
//   while (a < b) {
//     let temp = arr[a];
//     arr[a] = arr[b];
//     arr[b] = temp;
//     a++;
//     b--;
//   }
// }
// console.log(arr);

// ===========================================

// Move all zeros to the end of an array.

// let arr = [0, 1, 3, 0, 4, 5, 2, 2, 0, 0, 1, 1, 3, 0];

// let i = 0;
// let j = arr.length - 1;

// while (i != j) {
//   if (arr[i] == 0) {
//     let temp = arr[i];
//     arr[i] = arr[j];
//     arr[j] = temp;
//     j--;
//   } else {
//     i++;
//   }
// }

// console.log(arr);

// =====================================

// Find intersection of two arrays.

// let a = [10, 15, 22];
// let b = [15, 18, 22];
// let arr = []
// let k = 0;

// for (let i = 0; i < a.length; i++) {
//   for (let j = 0; j < b.length; j++) {
//     if (a[i] == b[j]) {
//       arr[k] = a[i];
//       k++
//       break;
//     }
//   }
// }
// console.log(arr);

// ==============================

// a2b4e4f2g3

// let s = "aabbbbeeeeffgg";
// let result = "";
// let count = 1;

// for (let i = 0; i < s.length; i++) {
//     if (s[i] === s[i + 1]) {
//         count++;
//     } else {
//         result = result + s[i] + count;
//         count = 1;
//     }
// }

// console.log("🚀 ~ result:", result)

// ==============================

// let matrix = [
//   [1, 2, 3, 4],
//   [5, 6, 7, 8],
//   [9, 10, 11, 12],
//   [13, 14, 15, 16],
//   [17, 18, 19, 20],
// ];

// function spiralTraversal(matrix) {
//     let result = [];
//     let rows = matrix.length;
//     let cols = matrix[0].length;

//     let top = 0, bottom = rows - 1;
//     let left = 0, right = cols - 1;

//     while (top <= bottom && left <= right) {
//         // Traverse from left to right
//         for (let i = left; i <= right; i++) {
//             result.push(matrix[top][i]);
//         }
//         top++;

//         // Traverse downwards
//         for (let i = top; i <= bottom; i++) {
//             result.push(matrix[i][right]);
//         }
//         right--;

//         if (top <= bottom) {
//             // Traverse from right to left
//             for (let i = right; i >= left; i--) {
//                 result.push(matrix[bottom][i]);
//             }
//             bottom--;
//         }

//         if (left <= right) {
//             // Traverse upwards
//             for (let i = bottom; i >= top; i--) {
//                 result.push(matrix[i][left]);
//             }
//             left++;
//         }
//     }
//     return result;
// }

// const spiralOrder = spiralTraversal(matrix);
// console.log(spiralOrder.join(' '));

// ==============================

let arr = [1, 2, 3, 3, 4, 1, 4, 5, 1, 2];

let counts = {};

for (let num of arr) {
    counts[num] = (counts[num] || 0) + 1;
}
Object.keys(counts)
        .sort((a, b) => a - b)
        .forEach(key => {
            console.log(`${key} occurs ${counts[key]} times`);
        });
console.log("🚀 ~ counts:", counts)