//
//  mobileApp.swift
//  mobile
//

import SwiftUI

@main
struct sem7projectApp: App {
    // @StateObject private var PhotoController = PhotoLoader(Collection: [], lastID: 0)
    var body: some Scene {
        WindowGroup {
            /*
            ContentView(task4data: $PhotoController.Collection,
                        loader: PhotoController
            )
                .task {
                    do {
                        try await PhotoController.LoadPhotoInfo()
                    }
                    catch {
                        fatalError(error.localizedDescription)
                    }
                }
             */
            ContentView()
        }
    }
}
