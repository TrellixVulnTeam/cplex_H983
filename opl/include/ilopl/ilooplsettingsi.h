// -------------------------------------------------------------- -*- C++ -*-
// File: ./include/ilopl/ilooplsettingsi.h
// --------------------------------------------------------------------------
// Licensed Materials - Property of IBM
//
// 5725-A06 5725-A29 5724-Y48 5724-Y49 5724-Y54 5724-Y55 
// Copyright IBM Corp. 1998, 2013
//
// US Government Users Restricted Rights - Use, duplication or
// disclosure restricted by GSA ADP Schedule Contract with
// IBM Corp.
// ---------------------------------------------------------------------------

#ifndef __OPL_ilooplsettingsiH
#define __OPL_ilooplsettingsiH

#ifdef _WIN32
#pragma pack(push, 8)
#endif


#ifndef __OPL_ilosysH
# include <ilopl/ilosys.h>
#endif
#ifndef __CONCERT_iloenvH
# include <ilconcert/iloenv.h>
#endif
// for the neum type...
#ifndef __OPL_ilooplprofileriH
# include <ilopl/ilooplprofileri.h>
#endif


#include <iostream>
//#include <string>
//#include <list>
//using namespace std;

class IloOplErrorHandlerI;
class IljVirtualMachine;
class IljIde;
class IloOplExecutionControllerI;
class IloOplProfilerI;
class IloOplProgressListenerI;
class IloOplResourceResolverI;

class IloOplModelI;
class IloOplSettingTable;
class IloOplLocationI;

class ILOOPL_EXPORTED IloOplSettingsI: public IloDestroyableI {
    IloOplErrorHandlerI* _handler;
    IljVirtualMachine* _vm;
    IloOplExecutionControllerI* _controller;
    IloOplResourceResolverI* _resolver;

    IljVirtualMachine* _ownVM;
    IljIde* _ownIde;
    IloOplExecutionControllerI* _defaultController;
    IloOplResourceResolverI* _ownResolver;
    IloOplProfilerI* _profiler;
    IloOplSettingTable* _table;
    IloOplProgressListenerI* _progress;
    IloBool _ownProgress;

    IloInt _refCount;

    void init();

private:
    friend class IloOplModelI;
    friend class IloOplSettings;
    void incrementRefCount();
    void decrementRefCount();

public:
    IloOplSettingsI(IloEnvI* env, IloOplErrorHandlerI& handler);
    IloOplSettingsI(IloEnvI* env, IloOplErrorHandlerI& handler, IljVirtualMachine& vm);
    ~IloOplSettingsI();

    IloOplErrorHandlerI& getErrorHandler() const;
    IljVirtualMachine* getVM() const;

    void setExecutionController(IloOplExecutionControllerI&);
    void removeExecutionController(IloOplExecutionControllerI&);
    IloOplExecutionControllerI& getExecutionController() const;

    IloOplSettingsI* clone() const;

public:
    IloOplSettingTable& getSettingTable() const {
        return *_table;
    }

    IloBool isWithLocations() const;
    void setWithLocations(IloBool with);

    IloBool isWithNames() const;
    void setWithNames(IloBool with);

    IloBool isWithWarnings() const;
    void setWithWarnings(IloBool with);

    IloBool isWithDebugInfo() const;
    void setWithDebugInfo(IloBool with);

	IloBool isCloudMode() const;
    void setCloudMode(IloBool with);

    IloBool isWithDataChecks() const;
    void setWithDataChecks(IloBool with);

    IloBool isForceElementUsage() const;
    void setForceElementUsage(IloBool onoff);

	IloBool isForceElementPostProcessingUsage() const;
	void setForceElementPostProcessingUsage(IloBool onoff);

    IloInt getDisplayWidth() const;
    void setDisplayWidth(IloInt value);

    IloInt getDisplayPrecision() const;
    void setDisplayPrecision(IloInt value);

    IloBool isDisplayWithIndex() const;
    void setDisplayWithIndex(IloBool with);

    IloBool isDisplayWithComponentName() const;
    void setDisplayWithComponentName(IloBool with);

    IloBool isDisplayOnePerLine() const;
    void setDisplayOnePerLine(IloBool onoff);

	IloInt getBigMapThreshold() const;
    void setBigMapThreshold(IloInt value);

    IloBool isMainEndEnabled() const;
    void setMainEndEnabled(IloBool value);

    IloBool isDelayExtraction() const;
    void setDelayExtraction(IloBool value);

    IloBool hasSlicingCache() const;
    void setSlicingCache(IloBool value);

    IloBool isMemoryEmphasis() const;
    void setMemoryEmphasis(IloBool value);

    IloBool isSkipAssert() const;
    void setSkipAssert(IloBool value);

	const char* getResolverPath() const;
	void setResolverPath(const char* path);

    IloBool isDistributedMIP() const;
	const char* getDistributedMIPConfig() const;
	void setDistributedMIPConfig(const char* path);

	IloBool isExportInternalData() const;
	const char* getExportInternalData() const;
	void setExportInternalData(const char* path);

	IloBool isExportExternalData() const;
	const char* getExportExternalData() const;
	void setExportExternalData(const char* path);

    IloInt getRelaxationLevel() const;
    void setRelaxationLevel(IloInt value);

    IloBool hasProfiler() const;
    IloOplProfilerI& getProfiler() const;
    void setProfiler(IloOplProfilerI& profiler);
    void removeProfiler();
    void enterProfilerSection(IloOplProfilerSection section, const char* name=0) const; 
    void exitProfilerSection (IloOplProfilerSection section) const;
    void exitProfilerSectionUser() const;
    void exitProfilerSectionOther() const;

    void enterProfilerInit(const char* name) const;
    void exitProfilerInit(const char* name) const;
    void enterProfilerExecute(const char* name) const;
    void exitProfilerExecute(const char* name) const;


    void setProfilerLocation(const IloOplLocationI& location) const;

    IloOplResourceResolverI& getResourceResolver() const;
    void setResourceResolver(IloOplResourceResolverI& resolver);

    IloBool isSkipWarnNeverUsedElements() const;
    void setSkipWarnNeverUsedElements(IloBool value);    

    IloBool isUseSortedSets() const;
    void setUseSortedSets(IloBool value);    

	const char* getTmpDir() const;
	void setTmpDir(const char* path);

    IloBool isKeepTmpFiles() const;
    void setKeepTmpFiles(IloBool value);    

    //  Run settings

    IloInt getRunMaxErrors() const;
    void setRunMaxErrors(IloInt max);

    IloInt getRunMaxWarnings() const;
    void setRunMaxWarnings(IloInt max);

    IloBool isRunProcessFeasibleSolutions() const;
    void setRunProcessFeasibleSolutions(IloBool flag);

    IloBool isOaaSProcessFeasibleSolutions() const;
    void setOaaSProcessFeasibleSolutions(IloBool flag);

    IloBool isRunDisplaySolution() const;
    void setRunDisplaySolution(IloBool flag);

    IloBool isRunDisplayRelaxations() const;
    void setRunDisplayRelaxations(IloBool flag);

    IloBool isRunDisplayConflicts() const;
    void setRunDisplayConflicts(IloBool flag);

    IloBool isRunDisplayProfile() const;
    void setRunDisplayProfile(IloBool flag);

    const char* getRunEngineLog() const;
    void setRunEngineLog(const char* log);

    IloBool isRunCallPopulate() const;
    void setRunCallPopulate(IloBool flag);

    const char* getRunEngineExportExtension() const;
    void setRunEngineExportExtension(const char* log);

    IloBool isUndefinedDataError() const;
    void setUndefinedDataError(IloBool flag);

    IloBool isWithMultiEnv() const;
    void setWithMultiEnv(IloBool flag);

	IloBool usesGC() const;
    void setGC(IloBool flag);


    void setProgressListener(IloOplProgressListenerI* l, IloBool transferOwnership=IloFalse);
    void removeProgressListener(IloOplProgressListenerI* l);
    IloOplProgressListenerI* getProgressListener() const;
    IloBool hasProgressListener() const;
};


inline IloOplErrorHandlerI& IloOplSettingsI::getErrorHandler() const {
    return *_handler;
}

inline IljVirtualMachine* IloOplSettingsI::getVM() const {
    return _vm;
}

inline void IloOplSettingsI::setProfiler(IloOplProfilerI& profiler) {
    _profiler = &profiler;
}
inline void IloOplSettingsI::removeProfiler() {
    _profiler = 0;
}
inline IloBool IloOplSettingsI::hasProfiler() const {
    return _profiler!=0;
}
inline IloOplProfilerI& IloOplSettingsI::getProfiler() const {
    return *_profiler;
}

class ILOOPL_EXPORTED IloOplExecutionControllerI: public IloRttiEnvObjectI {
    ILORTTIDECL
public:
    virtual ~IloOplExecutionControllerI();

    virtual std::ostream& getOut() const =0;
    virtual IloBool overrideBlock(const char* name) =0;
    virtual IloBool overrideMain(IloInt& status) =0;

    virtual void notifyNew(const IloOplModelI& opl) =0;
    virtual void notifyEnd(const IloOplModelI& opl) =0;
    virtual void notifyCall(const IloOplModelI& opl) =0;
    virtual void notifyReturn(const IloOplModelI& opl, IloBool status) =0;

    virtual void notifyNew(IloAlgorithmI& algorithm) =0;
    virtual void notifyEnd(IloAlgorithmI& algorithm) =0;
    virtual void notifyCall(IloAlgorithmI& algorithm) =0;
    virtual void notifyReturn(IloAlgorithmI& algorithm, IloBool status) =0;

    virtual void enableAbort(IloBool enable) =0;
    virtual void abort() =0;
protected:
    IloOplExecutionControllerI(IloEnvI* env);
};


class IloOplAbortHelper;

class ILOOPL_EXPORTED IloOplDefaultExecutionControllerI: public IloOplExecutionControllerI {
    ILORTTIDECL
private:
    std::ostream* _os;
    IloOplAbortHelper* _abort;

public:
    IloOplDefaultExecutionControllerI(IloEnvI* env);
    IloOplDefaultExecutionControllerI(IloEnvI* env, std::ostream& os);
    ~IloOplDefaultExecutionControllerI();

    void setOut(std::ostream& os);
    std::ostream& getOut() const;

    void enableAbort(IloBool enable);
    void abort();

    IloBool overrideBlock(const char* name);
    IloBool overrideMain(IloInt& status);

    void notifyNew(const IloOplModelI& opl);
    void notifyEnd(const IloOplModelI& opl);
    void notifyCall(const IloOplModelI& opl);
    void notifyReturn(const IloOplModelI& opl, IloBool status);

    void notifyNew(IloAlgorithmI& algorithm);
    void notifyEnd(IloAlgorithmI& algorithm);
    void notifyCall(IloAlgorithmI& algorithm);
    void notifyReturn(IloAlgorithmI& algorithm, IloBool status);
};

class IloOplModelSourceI;
class IloOplDataSourceI;
class IloStringArray;


class ILOOPL_EXPORTED IloOplResourceResolverI: public IloRttiEnvObjectI {
    ILORTTIDECL
    friend class IloOplSettingsI;
    IloOplSettingsI* _settings;
protected:
    IloOplResourceResolverI(IloEnvI* env);
    void setOplSettings(IloOplSettingsI* settings);
    virtual std::istream* doResolveStream(const char* base, const char* name) =0;

public:
    IloOplModelSourceI* resolveModelSource(const char* base, const char* name);
    IloOplDataSourceI* resolveDataSource(const char* base, const char* name);
    std::istream* resolveStream(const char* base, const char* name);
    virtual const char* resolvePath(const char* base, const char* name) =0;
	IloOplSettingsI* getOplSettings() const;
	
	void getSubstitutedResolverPaths(const char* basePath,IloStringArray& paths) const;
};



#ifdef _WIN32
#pragma pack(pop)
#endif

#endif

