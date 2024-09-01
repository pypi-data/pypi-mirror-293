/* ****************************************************************** **
**    OpenSees - Open System for Earthquake Engineering Simulation    **
**          Pacific Earthquake Engineering Research Center            **
**                                                                    **
** ****************************************************************** */
//
// Description: This file contains the class implementation for Vector.
//
// Written: fmk 
// Created: 11/96
// Revision: A
//
#include "Vector.h"
#include <iostream>
using std::nothrow;

#include <math.h>
#include <assert.h>
#include "blasdecl.h"

#if 0
#define VECTOR_BLAS
#endif

// Vector():
//        Standard constructor, sets size = 0;

Vector::Vector()
: sz(0), theData(0), fromFree(0)
{

}

// Vector(int size):
//        Constructor used to allocate a vector of size size.

Vector::Vector(int size)
: sz(size), theData(0), fromFree(0)
{
  assert(size >= 0);

  // get some space for the vector
  //  theData = (double *)malloc(size*sizeof(double));
  if (size > 0)
    theData = new double [size]{};

}


// Vector::Vector(double *data, int size)

Vector::Vector(double *data, int size)
: sz(size),theData(data),fromFree(1)
{

}
 


// Vector(const Vector&):
//        Constructor to init a vector from another.

Vector::Vector(const Vector &other)
: sz(other.sz),theData(0),fromFree(0)
{
  if (sz != 0) {
    theData = new double [other.sz];    
  }
  // copy the component data
  for (int i=0; i<sz; i++)
    theData[i] = other.theData[i];
}

// Vector(const Vector&):
//  Move constructor
#if !defined(NO_CXX11_MOVE)   
Vector::Vector(Vector &&other)
: sz(other.sz),theData(other.theData),fromFree(0)
{
  other.theData = nullptr;
  other.sz = 0;
} 
#endif


// ~Vector():
//         destructor, deletes the [] data

Vector::~Vector()
{
  if (theData != nullptr && fromFree == 0)
    delete [] theData;
  theData = nullptr;
}


int 
Vector::setData(double *newData, int size){
  if (theData != 0 && fromFree == 0) {
    delete [] theData;      
    theData = 0;
  }
  sz = size;
  theData = newData;
  fromFree = 1;

  if (sz <= 0) {
//    std::cerr << " Vector::Vector(double *, size) - size specified: " << size << " <= 0\n";
    sz = 0;
  }

  return 0;
}



int 
Vector::resize(int newSize){

  // first check that newSize is valid
  if (newSize < 0) {
//    std::cerr << "Vector::resize) - size specified " << newSize << " <= 0\n";
    return -1;
  } 
  
  // otherwise if newSize is gretaer than oldSize free old space and get new space
  else if (newSize > sz) {

    // delete the old array
    if (theData != 0 && fromFree == 0) {
      delete [] theData;
      theData = nullptr;
    }
    sz = 0;
    fromFree = 0;
    
    // create new memory
    // theData = (double *)malloc(newSize*sizeof(double));    
    theData = new double[newSize];

    sz = newSize;
  }  

  // just set the size to be newSize .. penalty of holding onto additional
  // memory .. but then save the free() and malloc() calls
  else 
    sz = newSize;    

  return 0;
}



    

int
Vector::Normalize(void) 
{
  double length = Norm();
  /*
  for (int i=0; i<sz; i++)
    length += theData[i] * theData[i];
  length = sqrt(length);
  */
  
  if (length == 0.0) 
    return -1;

  length = 1.0/length;
#ifdef VECTOR_BLAS
  const int incx = 1;
  dscal_(&sz, &length, theData, &incx);
#else
  for (int j=0; j<sz; j++)
    theData[j] *= length;
#endif
  return 0;
}

int
Vector::addVector(const Vector &other, double otherFact )
{
  // if sizes are compatable add
  assert(sz == other.sz);

  // check if quick return
  if (otherFact == 0.0)
    return 0; 

  else {
#ifdef VECTOR_BLAS
    const int incr = 1;
    daxpy_(&sz, &otherFact, other.theData, &incr, theData, &incr);
    return 0;
#else
    // want: this += other * otherFact
    double *dataPtr = theData;
    double *otherDataPtr = other.theData;
    if (otherFact == 1.0) { // no point doing a multiplication if otherFact == 1.0
      for (int i=0; i<sz; i++) 
        *dataPtr++ += *otherDataPtr++;
    } else if (otherFact == -1.0) { // no point doing a multiplication if otherFact == 1.0
      for (int i=0; i<sz; i++) 
        *dataPtr++ -= *otherDataPtr++;
    } else 
      for (int i=0; i<sz; i++) 
        *dataPtr++ += *otherDataPtr++ * otherFact;
#endif
  }

  // successfull
  return 0;
}
int
Vector::addVector(double thisFact, const Vector &other, double otherFact )
{
  // if sizes are compatable add
  assert(sz == other.sz);

  // check if quick return
  if (otherFact == 0.0 && thisFact == 1.0)
    return 0; 

  else if (thisFact == 1.0) {
#ifdef VECTOR_BLAS
    const int incr = 1;
    daxpy_(&sz, &otherFact, other.theData, &incr, theData, &incr);
    return 0;
#else
    // want: this += other * otherFact
    double *dataPtr = theData;
    double *otherDataPtr = other.theData;
    if (otherFact == 1.0) { // no point doing a multiplication if otherFact == 1.0
      for (int i=0; i<sz; i++) 
        *dataPtr++ += *otherDataPtr++;
    } else if (otherFact == -1.0) { // no point doing a multiplication if otherFact == 1.0
      for (int i=0; i<sz; i++) 
        *dataPtr++ -= *otherDataPtr++;
    } else 
      for (int i=0; i<sz; i++) 
        *dataPtr++ += *otherDataPtr++ * otherFact;
#endif
  }

  else if (thisFact == 0.0) {

    // want: this = other * otherFact
    double *dataPtr = theData;
    double *otherDataPtr = other.theData;
    if (otherFact == 1.0) { // no point doing a multiplication if otherFact == 1.0
      for (int i=0; i<sz; i++) 
        *dataPtr++ = *otherDataPtr++;
    } else if (otherFact == -1.0) { // no point doing a multiplication if otherFact == 1.0
      for (int i=0; i<sz; i++) 
        *dataPtr++ = -(*otherDataPtr++);
    } else 
      for (int i=0; i<sz; i++) 
        *dataPtr++ = *otherDataPtr++ * otherFact;
  }

  else {

    // want: this = this * thisFact + other * otherFact
    double *dataPtr = theData;
    double *otherDataPtr = other.theData;
    if (otherFact == 1.0) { // no point doing a multiplication if otherFact == 1.0
      for (int i=0; i<sz; i++) {
        double value = *dataPtr * thisFact + *otherDataPtr++;
        *dataPtr++ = value;
      }
    } else if (otherFact == -1.0) { // no point doing a multiplication if otherFact == 1.0
      for (int i=0; i<sz; i++) {
        double value = *dataPtr * thisFact - *otherDataPtr++;
        *dataPtr++ = value;
      }
    } else 
      for (int i=0; i<sz; i++) {
        double value = *dataPtr * thisFact + *otherDataPtr++ * otherFact;
        *dataPtr++ = value;
      }
  } 

  // successfull
  return 0;
}

// double Norm();
//        Method to return the norm of  vector. (non-const as may save norm for later)

double
Vector::Norm(void) const
{
  double value = 0;
  for (int i=0; i<sz; i++) {
    double data = theData[i];
    value += data*data;
  }
  return sqrt(value);
}

double
Vector::pNorm(int p) const
{
  double value = 0;
  
  if (p > 0) {
    for (int i=0; i<sz; i++) {
      double data = fabs(theData[i]);
      value += pow(data,p);
    }
    return pow(value,1.0/p);
  } else {
    for (int i=0; i<sz; i++) {
      double data = fabs(theData[i]);
      value = (data>value) ? data : value;
    }
    return value;
  }
}


double &
Vector::operator[](int x) 
{
  // check if it is inside range [0,sz-1]
  assert(x >= 0);
  
  if (x >= sz) {
    // TODO: Is this expected?
    double *dataNew = new (nothrow) double[x+1];
    for (int i=0; i<sz; i++)
      dataNew[i] = theData[i];
    for (int j=sz; j<x; j++)
      dataNew[j] = 0.0;
    
    if (fromFree == 0)
      if (theData != 0){
        delete [] theData;
      theData = 0;
    }
    theData = dataNew;
    sz = x+1;
  }

  return theData[x];
}

double Vector::operator[](int x) const
{
  // check if it is inside range [0,sz-1]
  assert(x >= 0 && x < sz);
  return theData[x];
}


// Vector &operator=(const Vector  &V):
//        the assignment operator, This is assigned to be a copy of V. if sizes
//        are not compatable this.theData [] is deleted. The data pointers will not
//        point to the same area in mem after the assignment.
//

Vector &
Vector::operator=(const Vector &V) 
{
  // first check we are not trying v = v
  if (this != &V) {

      if (sz != V.sz)  {
#ifdef _G3DEBUG
//          std::cerr << "Vector::operator=() - vectors of differing sizes\n";
#endif

          // Check that we are not deleting an empty Vector
          if (this->theData != 0){
            delete [] this->theData;
            this->theData = 0;
          }
          this->sz = V.sz;
          
          // Check that we are not creating an empty Vector
          theData = (sz != 0) ? new double[sz] : nullptr;
      }
      // copy the data
      for (int i=0; i<sz; i++)
        theData[i] = V.theData[i];
  }

  return *this;
}

// Move assignment operator.  
#if !defined(NO_CXX11_MOVE)   
Vector &
Vector::operator=(Vector &&V) 
{
  // first check we are not trying v = v
  if (this != &V) {
    if (this->theData != nullptr) { 
      delete [] this->theData;
      this->theData = 0;
    }
    theData = V.theData;
    this->sz = V.sz;
    V.theData = 0;
    V.sz = 0;
  }
  return *this;
}
#endif


// Vector &operator+=(double fact):
//        The += operator adds fact to each element of the vector, data[i] = data[i]+fact.

Vector &Vector::operator+=(double fact)
{
  if (fact != 0.0)
    for (int i=0; i<sz; i++)
      theData[i] += fact;
  return *this;    
}


// Vector &operator-=(double fact)
//        The -= operator subtracts fact from each element of the vector, data[i] = data[i]-fact.

Vector &Vector::operator-=(double fact)
{
  if (fact != 0.0)
    for (int i=0; i<sz; i++)
      theData[i] -= fact;
  return *this;    
}



// Vector &operator*=(double fact):
//        The -= operator subtracts fact from each element of the vector, data[i] = data[i]-fact.

Vector &Vector::operator*=(double fact)
{
#ifdef VECTOR_BLAS
  const int incr = 1;
  dscal_(&sz, &fact, theData, &incr);
  return *this;
#else
  for (int i=0; i<sz; i++)
    theData[i] *= fact;
  return *this;
#endif
}


// Vector &operator/=(double fact):
//        The /= operator divides each element of the vector by fact, theData[i] = theData[i]/fact.
//        Program exits if divide-by-zero would occur with warning message.

Vector &Vector::operator/=(double fact)
{

    for (int i=0; i<sz; i++)
      theData[i] /= fact;

  return *this;
}




// Vector operator+(double fact):
//        The + operator returns a Vector of the same size as current, whose components
//        are return(i) = theData[i]+fact;

Vector 
Vector::operator+(double fact) const
{
  Vector result(*this);
  if (result.Size() != sz) 
//    std::cerr << "Vector::operator+(double) - ran out of memory for new Vector\n";

  result += fact;
  return result;
}



// Vector operator-(double fact):
//        The + operator returns a Vector of the same size as current, whose components
//        are return(i) = theData[i]-fact;

Vector 
Vector::operator-(double fact) const
{
    Vector result(*this);
    if (result.Size() != sz) 
//      std::cerr << "Vector::operator-(double) - ran out of memory for new Vector\n";

    result -= fact;
    return result;
}



// Vector operator*(double fact):
//        The + operator returns a Vector of the same size as current, whose components
//        are return(i) = theData[i]*fact;

Vector 
Vector::operator*(double fact) const
{
    Vector result(*this);
    if (result.Size() != sz) 
//      std::cerr << "Vector::operator*(double) - ran out of memory for new Vector\n";

    result *= fact;
    return result;
}


// Vector operator/(double fact):
//        The + operator returns a Vector of the same size as current, whose components
//        are return(i) = theData[i]/fact; Exits if divide-by-zero error.

Vector 
Vector::operator/(double fact) const
{
    if (fact == 0.0) 
      ;
//      std::cerr << "Vector::operator/(double fact) - divide-by-zero error coming\n";

    Vector result(*this);


    result /= fact;
    return result;
}



// Vector &operator+=(const Vector &V):
//        The += operator adds V's data to data, data[i]+=V(i). A check to see if
//        vectors are of same size is performed if VECTOR_CHECK is defined.

Vector &
Vector::operator+=(const Vector &other)
{
#ifdef _G3DEBUG
  if (sz != other.sz) {
//    std::cerr << "WARNING Vector::operator+=(Vector):Vectors not of same sizes: " << sz << " != " << other.sz << "\n";
    return *this;
  }    
#endif

  for (int i=0; i<sz; i++)
    theData[i] += other.theData[i];
  return *this;            
}



// Vector &operator-=(const Vector &V):
//        The -= operator subtracts V's data from  data, data[i]+=V(i). A check 
//           to see if vectors are of same size is performed if VECTOR_CHECK is defined.

Vector &
Vector::operator-=(const Vector &other)
{
#ifdef _G3DEBUG
  if (sz != other.sz) {
//    std::cerr << "WARNING Vector::operator+=(Vector):Vectors not of same sizes: " << sz << " != " << other.sz << "\n";
    return *this;
  }
#endif
  
  for (int i=0; i<sz; i++)
    theData[i] -= other.theData[i];
  return *this;    
}



// Vector operator+(const Vector &V):
//        The + operator checks the two vectors are of the same size if VECTOR_CHECK is defined.
//         Then returns a Vector whose components are the vector sum of current and V's data.

Vector 
Vector::operator+(const Vector &b) const
{
#ifdef _G3DEBUG
  if (sz != b.sz) {
//    std::cerr << "WARNING Vector::operator+=(Vector):Vectors not of same sizes: " << sz << " != " << b.sz << "\n";
    return *this;
  }
#endif

    Vector result(*this);

    // check new Vector of correct size
  if (result.Size() != sz) {
//    std::cerr << "Vector::operator-(Vector): new Vector not of correct size \n";
    return result;
  }
  result += b;
  return result;
}


// Vector operator-(const Vector &V):
//        The - operator checks the two vectors are of the same size and then returns a Vector
//        whose components are the vector difference of current and V's data.

Vector 
Vector::operator-(const Vector &b) const
{
#ifdef _G3DEBUG
  if (sz != b.sz) {
//    std::cerr << "WARNING Vector::operator+=(Vector):Vectors not of same sizes: " << sz << " != " << b.sz << "\n";
    return *this;
  }
#endif

  Vector result(*this);

  // check new Vector of correct size
  if (result.Size() != sz) {
//    std::cerr << "Vector::operator-(Vector): new Vector not of correct size \n";
    return result;
  }

  result -= b;
  return result;
}



// double operator^(const Vector &V) const;
//        Method to perform (Vector)transposed * vector.
double
Vector::operator^(const Vector &V) const
{
#ifdef _G3DEBUG
  if (sz != V.sz) {
//    std::cerr << "WARNING Vector::operator+=(Vector):Vectors not of same sizes: " << sz << " != " << V.sz << "\n";
    return 0.0;
  }
#endif

  double result = 0.0;
  double *dataThis = theData;
  double *dataV = V.theData;
    for (int i=0; i<sz; i++)
      result += *dataThis++ * *dataV++;

    return result;
}

        
// Vector operator==(const Vector &V):
//        The == operator checks the two vectors are of the same size if VECTOR_CHECK is defined.
//         Then returns 1 if all the components of the two vectors are equal and 0 otherwise.

int 
Vector::operator==(const Vector &V) const
{
  if (sz != V.sz)
    return 0;

  double *dataThis = theData;
  double *dataV = V.theData;

  for (int i=0; i<sz; i++)
    if (*dataThis++ != *dataV++)
      return 0;

  return 1;
}

int 
Vector::operator==(double value) const
{
  double *dataThis = theData;

  for (int i=0; i<sz; i++)
    if (*dataThis++ != value)
      return 0;

  return 1;
}


// Vector operator!=(const Vector &V):
//        The != operator checks the two vectors are of the same size if VECTOR_CHECK is defined.
//         Then returns 1 if any of the components of the two vectors are unequal and 0 otherwise.

int
Vector::operator!=(const Vector &V) const
{
  if (sz != V.sz)
    return 1;

  double *dataThis = theData;
  double *dataV = V.theData;

  for (int i=0; i<sz; i++)
    if (*dataThis++ != *dataV++)
      return 1;

  return 0;
}

int 
Vector::operator!=(double value) const
{
  double *dataThis = theData;

  for (int i=0; i<sz; i++)
    if (*dataThis++ != value)
      return 1;

  return 0;
}

Vector operator*(double a, const Vector &V)
{
  return V * a;
}


int
Vector::Assemble(const Vector &V, int init_pos, double fact) 
{
  int res = 0;
  int cur_pos   = init_pos;  
  int final_pos = init_pos + V.sz - 1;
  
  if ((init_pos >= 0) && (final_pos < sz)) {
     for (int j=0; j<V.sz; j++) 
        (*this)(cur_pos++) += V(j)*fact;
  }
  else {
//     std::cerr << "WARNING: Vector::Assemble(const Vector &V, int init_pos, double fact): ";
//     std::cerr << "position outside bounds \n";
     res = -1;
  }

  return res;
}

int
Vector::Extract(const Vector &V, int init_pos, double fact) 
{
  int res = 0;
  int cur_pos   = init_pos;  
  int final_pos = init_pos + sz - 1;
  
  if ((init_pos >= 0) && (final_pos < V.sz))
  {
     for (int j=0; j<sz; j++) 
        (*this)(j) = V(cur_pos++)*fact;
  }
  else 
  {
//     std::cerr << "WARNING: Vector::Assemble(const Vector &V, int init_pos, double fact): ";
//     std::cerr << "position outside bounds \n";
     res = -1;
  }

  return res;
}

