/* ****************************************************************** **
**    OpenSees - Open System for Earthquake Engineering Simulation    **
**          Pacific Earthquake Engineering Research Center            **
**                                                                    **
**                                                                    **
** (C) Copyright 1999, The Regents of the University of California    **
** All Rights Reserved.                                               **
**                                                                    **
** Commercial use of this program without express permission of the   **
** University of California, Berkeley, is strictly prohibited.  See   **
** file 'COPYRIGHT'  in main directory for information on usage and   **
** redistribution,  and for a DISCLAIMER OF ALL WARRANTIES.           **
**                                                                    **
** Developed by:                                                      **
**   Frank McKenna (fmckenna@ce.berkeley.edu)                         **
**   Gregory L. Fenves (fenves@ce.berkeley.edu)                       **
**   Filip C. Filippou (filippou@ce.berkeley.edu)                     **
**                                                                    **
** ****************************************************************** */
//
// Written: fmk
// $Date: 2010-03-05 22:32:36 $
// /usr/local/cvs/OpenSees/SRC/api/elementAPI.h
//

#ifndef _eleAPI
#define _eleAPI

#define ISW_INIT 0
#define ISW_COMMIT 1
#define ISW_REVERT 2
#define ISW_FORM_TANG_AND_RESID 3
#define ISW_FORM_MASS 4
#define ISW_REVERT_TO_START 5
#define ISW_DELETE 6

#define ISW_SET_RESPONSE 7
#define ISW_GET_RESPONSE 8

#define OPS_UNIAXIAL_MATERIAL_TYPE 1
#define OPS_SECTION2D_TYPE 2
#define OPS_SECTION3D_TYPE 3
#define OPS_PLANESTRESS_TYPE 4
#define OPS_PLANESTRAIN_TYPE 5
#define OPS_THREEDIMENSIONAL_TYPE 6
#define OPS_SECTION_TYPE 7

struct modState {
    double time;
    double dt;
};

typedef struct modState modelState;

typedef void (*matFunct)(struct matObject*, modelState*, double* strain, double* tang, double* stress, int* isw, int* error);

struct matObject {
    int tag;
    int matType;
    int nParam;
    int nState;
    double* theParam;
    double* cState;
    double* tState;
    matFunct matFunctPtr;
    void* matObjectPtr;
};

typedef struct matObject matObj;

typedef void (*eleFunct)(struct eleObject*, modelState*, double* tang, double* resid, int* isw, int* error);

struct eleObject {
    int tag;
    int nNode;
    int nDOF;
    int nParam;
    int nState;
    int nMat;
    int* node;
    double* param;
    double* cState;
    double* tState;
    matObj** mats;
    eleFunct eleFunctPtr;
};

typedef struct eleObject eleObj;

class AnalysisModel;
class EquiSolnAlgo;
class ConstraintHandler;
class DOF_Numberer;
class LinearSOE;
class EigenSOE;
class StaticAnalysis;
class DirectIntegrationAnalysis;
class VariableTimeStepDirectIntegrationAnalysis;
class StaticIntegrator;
class TransientIntegrator;
class ConvergenceTest;

#define OPS_Error ops_error_
#define OPS_GetIntInput ops_getintinput_
#define OPS_GetDoubleInput ops_getdoubleinput_
#define OPS_SetDoubleListsOutput ops_setdoublelistsoutput_
#define OPS_SetDoubleDictOutput ops_setdoubledictoutput_
#define OPS_SetDoubleDictListOutput ops_setdoubledictlistoutput_
//
#define OPS_AllocateMaterial ops_allocatematerial_
#define OPS_AllocateElement ops_allocateelement_
#define OPS_GetMaterialType ops_getmaterialtype_
#define OPS_GetMaterial ops_getmaterial_
#define OPS_GetMaterialPtr ops_getmaterialptr_
#define OPS_GetCrdTransf ops_getcrdtransf_
#define OPS_GetFrictionModel ops_getfrictionmodel_
#define OPS_GetNodeCrd ops_getnodecrd_
#define OPS_GetNodeDisp ops_getnodedisp_
#define OPS_GetNodeVel ops_getnodevel_
#define OPS_GetNodeAccel ops_getnodeaccel_
#define OPS_GetNodeIncrDisp ops_getnodeincrdisp_
#define OPS_GetNodeIncrDeltaDisp ops_getnodeincrdeltadisp_
#define OPS_InvokeMaterial ops_invokematerial_
#define OPS_InvokeMaterialDirectly ops_invokematerialdirectly_
#define OPS_GetInt ops_getintinput_
#define OPS_GetDouble ops_getdoubleinput_
#define OPS_GetString ops_getstring
#define OPS_GetStringFromAll ops_getstringfromall_
#define OPS_SetString ops_setstring
#define OPS_GetNDM ops_getndm_
#define OPS_GetNDF ops_getndf_
#define OPS_GetFEDatastore ops_getfedatastore_
#define OPS_GetInterpPWD ops_getinterppwd_

#define OPS_GetAnalysisModel ops_getanalysismodel_
#define OPS_GetVariableTimeStepTransientAnalysis ops_getvariabletimesteptransientanalysis_
#define OPS_GetNumEigen ops_getnumeigen_
#define OPS_GetStaticIntegrator ops_getstaticintegrator_
#define OPS_GetTest ops_gettest_
#define OPS_builtModel ops_builtmodel_
#define OPS_GetDomain ops_getdomain_


#ifdef __cplusplus
#include <map>
#include <vector>
extern "C" int         OPS_GetNDM();
extern "C" int         OPS_GetNDF();
extern "C" int         OPS_Error(const char* errorMessage, int length);
extern "C" int         OPS_GetNumRemainingInputArgs();
extern "C" int         OPS_ResetCurrentInputArg(int cArg);
extern "C" int         OPS_GetIntInput(int* numData, int* data);
extern "C" int         OPS_GetDoubleInput(int* numData, double* data);
extern "C" const char* OPS_GetString(); // does a strcpy
extern "C" const char* OPS_GetStringFromAll(char* buffer, int len); // does a strcpy
extern "C" int         OPS_SetString(const char* str);
extern "C" int         OPS_GetStringCopy(char** cArray); // returns a new copy

extern "C" int         OPS_SetDoubleListsOutput(std::vector<std::vector<double>>& data);
extern "C" int         OPS_SetDoubleDictOutput(std::map<const char*, double>& data);
extern "C" int         OPS_SetDoubleDictListOutput(std::map<const char*, std::vector<double>>& data);

class UniaxialMaterial;
class NDMaterial;
class SectionForceDeformation;
class CrdTransf;
class FrictionModel;
// class LimitCurve;
class Domain;
class FE_Datastore;
#if !defined(OPS_USE_RUNTIME)
  UniaxialMaterial* OPS_GetUniaxialMaterial(int matTag);
  Domain* OPS_GetDomain(void);
  AnalysisModel** OPS_GetAnalysisModel(void);
#endif
extern NDMaterial* OPS_GetNDMaterial(int matTag);
extern SectionForceDeformation* OPS_GetSectionForceDeformation(int secTag);
extern CrdTransf* OPS_GetCrdTransf(int crdTag);
extern FrictionModel* OPS_GetFrictionModel(int frnTag);

extern FE_Datastore* OPS_GetFEDatastore();
extern "C" const char* OPS_GetInterpPWD();

extern "C" bool* OPS_builtModel(void);
int OPS_numIter();


#else // __cplusplus

int     OPS_GetNDF();
int     OPS_GetNDM();

int     OPS_Error(const char*, int length);
int     OPS_GetIntInput(int* numData, int* data);
int     OPS_GetDoubleInput(int* numData, double* data);
int     OPS_GetString(char* cArray, int sizeArray);
ConstraintHandler** OPS_GetHandler(void);
EigenSOE** OPS_GetEigenSOE(void);
int* OPS_GetNumEigen(void);
bool* OPS_builtModel(void);

#endif // __cplusplus

#endif // _eleAPI
